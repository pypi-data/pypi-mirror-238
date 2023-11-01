import ast
import itertools
import logging
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import warnings
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Literal, Optional, Set, Union

import packaging.tags
import packaging.utils
import pkginfo
import setuptools
from packaging.requirements import Requirement  # noqa: F401
from packaging.specifiers import SpecifierSet  # noqa: F401
from packaging.version import Version

from . import ty
from .appdirs import user_cache_dir

logger = logging.getLogger(__name__)

RecipeSourceKind = Literal["wheel", "distribution"]


class RecipeBuildVenvCreationFailed(Exception):
    pass


class RecipeSource(object):
    path: Path

    @classmethod
    def from_path(cls, path: Union[Path, str]) -> Optional["RecipeSource"]:
        if isinstance(path, str):
            path = Path(path)
        kind = cls._infer_kind(path)
        if kind == "wheel":
            return WheelSource(path)
        elif kind == "distribution":
            return DirectorySource(path)
        else:
            return None

    def __init__(
        self,
        path: Path,
    ):
        self.path = path

    @classmethod
    def _infer_kind(cls, path: Path) -> Optional[RecipeSourceKind]:
        if path.is_file() and path.suffix == ".whl":
            return "wheel"

        if path.is_dir() and (
            (path / "setup.py").is_file() or (path / "pyproject.toml").is_file()
        ):
            return "distribution"
        return None

    @cached_property
    def path_kind(self):
        return self._infer_kind(self.path)

    @cached_property
    def version(self) -> Optional[Version]:
        ...

    @cached_property
    def distribution_name(self) -> str:
        ...

    @cached_property
    def package_name(self) -> str:
        # TODO: this should be the name of the top level package, not the
        # distribution/wheel.
        assert self.distribution_name is not None

        package_name = re.sub(r"[^\w\d.]+", "_", self.distribution_name, re.UNICODE)
        return package_name

    @cached_property
    def pkginfo_metadata(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            maybe_pkginfo = pkginfo.get_metadata(str(self.path.resolve()))
            if maybe_pkginfo is not None and maybe_pkginfo.name is not None:
                return maybe_pkginfo
        return None

    @cached_property
    def requirements(self) -> Optional[Set[Requirement]]:
        if self.pkginfo_metadata is None:
            return None
        return set(Requirement(line) for line in self.pkginfo_metadata.requires_dist)


class WheelSource(RecipeSource):
    @cached_property
    def wheel_info(self) -> pkginfo.Wheel:
        metadata = self.pkginfo_metadata
        assert isinstance(
            metadata, pkginfo.Wheel
        ), f"expected pkginfo metadata to be Wheel, got {type(metadata)}"
        return metadata

    @cached_property
    def distribution_name(self) -> str:
        return self.wheel_info.name

    @cached_property
    def version(self) -> Version:
        return Version(self.wheel_info.version)

    def to_file_uri(self) -> str:
        return self.path.resolve().as_uri()


class DirectorySource(RecipeSource):
    def __init__(self, directory: Path):
        super().__init__(directory)
        # TODO: infer correctly
        name = self.package_name
        name_as_path = name.replace(".", os.sep)
        pkg_dir = directory / name_as_path
        src_pkg_dir = directory / "src" / name_as_path

        existing = set()
        if pkg_dir.is_dir():
            self.pkg_dir = pkg_dir
            self.prefix = ""
            existing.add(pkg_dir)
        if src_pkg_dir.is_dir():
            self.pkg_dir = src_pkg_dir
            self.prefix = "src"
            existing.add(src_pkg_dir)

        if len(existing) > 1:
            raise ValueError(
                "Multiple matches for package name {}: {}".format(
                    name, ", ".join([str(p) for p in sorted(existing)])
                )
            )
        elif not existing:
            raise ValueError("No package directory found for module {}".format(name))

        self.source_dir = directory / self.prefix
        self.directory = directory

        if "." in name:
            logger.warn(
                "Package name %s contains a dot and may not work as intended.", name
            )
            self.namespace_package_name = name.rpartition(".")[0]
            self.in_namespace_package = True

    @cached_property
    def version(self) -> Optional[Version]:
        from_ast = get_version_from_ast(self)
        if from_ast is not None:
            return Version(from_ast)
        # TODO: import in a subprocess or just build metadata eagerly using _build_meta
        # from_import = get_version_from_import(self)
        # if from_import is not None:
        #     return Version(from_import)
        return None

    @cached_property
    def distribution_name(self) -> str:
        cached_metadata = self.pkginfo_metadata
        if cached_metadata is not None:
            return cached_metadata.name
        # TODO: we probably need to do a wheel build to be sure
        distribution_name = re.sub(
            r"[^\w\d]+", "_", self.package_name, re.UNICODE
        ).replace("_", "-")
        return distribution_name

    @cached_property
    def discovered_packages(self):
        all_discovered = setuptools.find_packages(
            where=str(self.path), exclude=("tests", "tests.*")
        )
        return [p for p in all_discovered if p.find(".") == -1]

    @cached_property
    def package_name(self):
        discovered_packages = self.discovered_packages
        if len(discovered_packages) == 1:
            return discovered_packages[0]
        elif len(discovered_packages) == 0:
            raise ValueError(
                f"Could not infer package name from directory: {self.path}"
            )
        else:
            raise ValueError(
                f"Found multiple packages in directory {self.path}: {discovered_packages}"
            )

    @property
    def file(self):
        return self.pkg_dir / "__init__.py"

    @property
    def version_files(self):
        paths = [self.pkg_dir / "__init__.py"]
        for filename in ("about.py", "version.py", "_version.py", "__version__.py"):
            if (self.pkg_dir / filename).is_file():
                paths.insert(0, self.pkg_dir / filename)
        return paths

    def iter_files(self):
        def _include(path):
            name = os.path.basename(path)
            if (name == "__pycache__") or name.endswith(".pyc"):
                return False
            return True

        for dirpath, dirs, files in os.walk(str(self.pkg_dir)):
            for file in sorted(files):
                full_path = os.path.join(dirpath, file)
                if _include(full_path):
                    yield full_path

            dirs[:] = [d for d in sorted(dirs) if _include(d)]


def get_version_from_ast(target: DirectorySource):
    def _extract_version_assignment(node: ast.stmt) -> Optional[ast.Assign]:
        if not isinstance(node, ast.Assign):
            return None
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__version__":
                # TODO: multiple assignment?
                return node
        return None

    def _extract_literal_version(node: ast.Assign) -> Optional[str]:
        if isinstance(node.value, ast.Str):
            return node.value.s
        return None

    version = None
    node = None
    for version_path in target.version_files:
        with version_path.open("rb") as f:
            node = ast.parse(f.read())
        for child in node.body:
            assignment = _extract_version_assignment(child)
            if assignment is not None:
                version = _extract_literal_version(assignment)
                if version is not None:
                    break
            else:
                # programmatically generated version - we need to use imports
                pass
    assert node is not None, f"no __version__ found in module {target.package_name}"
    return version


_IMPORT_COUNTER = 0


def get_version_from_import(target: DirectorySource):
    """
    Import the module and extract the version from it.
    """
    global _IMPORT_COUNTER
    from importlib.util import module_from_spec, spec_from_file_location

    @contextmanager
    def stash_global_state():
        """
        Stash global state that modules might change at import time.

        TODO: Can we stash sys.modules, recipe registry, here?
        """
        logging_handlers = logging.root.handlers[:]
        try:
            yield
        finally:
            logging.root.handlers = logging_handlers

    _IMPORT_COUNTER += 1

    mod_name = f"prodigy_teams.imported_recipe.{_IMPORT_COUNTER}"
    spec = spec_from_file_location(mod_name, target.file)
    assert spec is not None, f"Failed to load module from {target.file}"
    assert spec.loader is not None
    with stash_global_state():
        m = module_from_spec(spec)
        sys.modules[mod_name] = m
        try:
            spec.loader.exec_module(m)
        finally:
            imported_mods = [mod for mod in sys.modules if mod.startswith(mod_name)]
            for mod in imported_mods:
                sys.modules.pop(mod, None)

    version = m.__dict__.get("__version__", None)
    return version


def get_version_from_pkginfo(target: DirectorySource):
    """
    Get the version from the .egg-info/.dist-info folders

    This version is computed when the package is built, so it's not
    necessarily the same as the version in the source code.
    """

    meta = pkginfo.get_metadata(str(target.source_dir))
    assert meta is not None
    return meta.version


class VenvError(Exception):
    pass


class InvalidVenvPath(VenvError):
    pass


class InvalidVenvError(VenvError):
    def __init__(
        self,
        venv_dir: Path,
        python_bin: ty.Optional[Path] = None,
        activate_script: ty.Optional[Path] = None,
    ):
        self.venv_dir = venv_dir
        self.python_bin = python_bin
        self.activate_script = activate_script
        super().__init__(
            f"Invalid venv: {venv_dir} ({python_bin=}, {activate_script=})"
        )


class PythonVersionError(VenvError):
    def __init__(
        self,
        venv_dir: Path,
        actual_version: str,
        required_version: str,
    ):
        self.venv_dir = venv_dir
        self.actual_version = actual_version
        self.required_version = required_version
        super().__init__(
            f"Invalid python version: {venv_dir} - version is {actual_version} but required {required_version}"
        )


class VenvCreationError(VenvError):
    def __init__(
        self, venv_dir: Path, build_venv: "Venv", error: subprocess.CalledProcessError
    ):
        self.venv_dir = venv_dir
        python_bin = Venv._find_python_bin(venv_dir)
        activate_script = Venv._find_activate(venv_dir)
        self.python_bin = python_bin
        self.activate_script = activate_script
        message = f"""Unexpected failure while creating virtualenv:
        ### Error: {error.__class__.__name__}
        cmd: {str(error.cmd)}
        return code: {str(error.returncode)}
        ### Stdout
        {error.stdout}
        ### Stderr
        {error.stderr}

        ### Debug Info:
        build_venv: {build_venv.python}
        - {Path(build_venv.python).exists()=}
        - {Path(build_venv.python).is_file()=}

        cached_venv: {str(venv_dir.absolute())}
        - {venv_dir=} ({"exists" if venv_dir and venv_dir.exists() else "not found"})
        - {python_bin=} ({"exists" if python_bin and python_bin.exists() else "not found"})
        - {activate_script=} ({"exists" if activate_script and activate_script.exists() else "not found"})
        """
        super().__init__(message)


class Venv:
    def __init__(
        self,
        python_binary: str,
        activate_script: ty.Optional[Path],
        venv_dir: ty.Optional[Path],
        cwd: ty.Optional[Path] = None,
    ) -> None:
        self.python = python_binary
        self.activate_script = activate_script
        self.venv_dir = venv_dir
        self._default_cwd = cwd

    @classmethod
    def init_from_dir(
        cls,
        venv_dir: Path,
        cwd: ty.Optional[Path],
        require_python_version: ty.Optional[str] = None,
    ) -> "Venv":
        python_bin, activate_script = cls._validate_venv(
            venv_dir, require_python_version=require_python_version
        )
        return Venv(str(python_bin), activate_script, venv_dir=venv_dir, cwd=cwd)

    @classmethod
    @contextmanager
    def from_active(cls, cwd: ty.Optional[Path]) -> ty.Iterator["Venv"]:
        yield cls(sys.executable, None, venv_dir=None, cwd=cwd)

    @classmethod
    @contextmanager
    def temporary(cls, cwd: ty.Optional[Path] = None) -> ty.Iterator["Venv"]:
        with _make_tempdir() as tmp:
            venv_path = Path(tmp) / "venv"
            with cls.from_active(cwd=cwd) as build_venv:
                yield build_venv.create_venv(venv_path, cwd=cwd)

    @classmethod
    def _get_venv_cache_path(cls, package_name: str, mkdir: bool = False) -> Path:
        cache_key = (package_name,)
        cache_base_path = _get_venvs_cache_path()
        cached_venv = (cache_base_path / "+".join(cache_key)).absolute()
        if mkdir:
            cached_venv.parent.mkdir(exist_ok=True, parents=True)
        return cached_venv

    def create_or_activate_venv(
        self,
        venv_path: Path,
        cwd: ty.Optional[Path] = None,
        fill_existing_dir: bool = False,
        require_python_version: ty.Optional[str] = None,
    ) -> "Venv":
        is_empty_dir = venv_path.is_dir() and len(os.listdir(venv_path)) == 0
        try_fill = fill_existing_dir and Venv._is_venv_dir(venv_path)
        if not venv_path.exists() or is_empty_dir or try_fill:
            with self.from_active(cwd=cwd) as build_venv:
                return build_venv.create_venv(venv_path, cwd=cwd)
        elif venv_path.is_dir():
            return Venv.init_from_dir(
                venv_path, cwd=cwd, require_python_version=require_python_version
            )
        else:
            raise InvalidVenvPath(f"Cannot create venv, path is a file: {venv_path}")

    def create_venv(self, venv_path: Path, cwd: ty.Optional[Path] = None) -> "Venv":
        try:
            _subprocess_run(
                [sys.executable, "-m", "venv", str(venv_path.absolute())],
                cwd or Path.cwd(),
            )
        except subprocess.CalledProcessError as e:
            raise VenvCreationError(venv_dir=venv_path, build_venv=self, error=e)
        return Venv.init_from_dir(venv_path, cwd=cwd)

    @classmethod
    def _is_venv_dir(cls, venv_path: Path) -> bool:
        if not venv_path.is_dir():
            return False
        python_bin = cls._find_python_bin(venv_path)
        activate_script = cls._find_activate(venv_path)
        return (
            python_bin is not None
            and python_bin.exists()
            or activate_script is not None
            and activate_script.exists()
        )

    @classmethod
    def _validate_venv(
        cls, venv_path: Path, require_python_version: ty.Optional[str] = None
    ) -> ty.Tuple[Path, Path]:
        python_bin = cls._find_python_bin(venv_path)
        activate_script = cls._find_activate(venv_path)
        if (
            python_bin is None
            or not python_bin.exists()
            or activate_script is None
            or not activate_script.exists()
        ):
            raise InvalidVenvError(
                venv_path, python_bin=python_bin, activate_script=activate_script
            )
        if require_python_version:
            try:
                output = _subprocess_run(
                    [str(python_bin.absolute()), "--version"], cwd=Path.cwd()
                ).stdout
                observed_version = output.split()[1]
                if not observed_version.startswith(require_python_version):
                    raise PythonVersionError(
                        venv_path,
                        actual_version=observed_version,
                        required_version=require_python_version,
                    )
            except Exception as e:
                raise InvalidVenvError(
                    venv_path, python_bin=python_bin, activate_script=activate_script
                ) from e

        return python_bin, activate_script

    @classmethod
    def _find_python_bin(cls, venv_base: Path) -> Optional[Path]:
        if sys.platform == "win32":
            return venv_base / "Scripts" / "python.exe"
        else:
            for candidate in ["local/bin", "bin"]:
                bin_path = venv_base / candidate / "python"
                if bin_path.exists():
                    return bin_path
        return None

    @classmethod
    def _find_activate(cls, venv_base: Path) -> Optional[Path]:
        if sys.platform == "win32":
            subdirs = ["Scripts"]
            bin_names = ["activate", "activate.bat"]
        else:
            subdirs = ["local/bin", "bin"]
            bin_names = ["activate", "activate.sh"]
        for subdir_candidate in subdirs:
            for bin_candidate in bin_names:
                bin_path = venv_base / subdir_candidate / bin_candidate
                if bin_path.exists():
                    return bin_path
        return None

    def cwd(self, override: ty.Optional[Path] = None) -> Path:
        return override or self._default_cwd or Path.cwd()

    def install(
        self,
        *packages: str,
        upgrade: bool = False,
        no_deps: bool = False,
        find_links: ty.List[Path] = [],
        cwd: ty.Optional[Path] = None,
        force_reinstall: bool = False,
    ) -> subprocess.CompletedProcess:
        args = [self.python, "-m", "pip", "install"]
        args.append("--disable-pip-version-check")
        if upgrade:
            args.append("--upgrade")
        if no_deps:
            args.append("--no-deps")
        if force_reinstall:
            args.append("--force-reinstall")
        if find_links:
            for dir in find_links:
                args.extend(["-f", str(dir)])
        args.extend(packages)
        return _subprocess_run(args, self.cwd(cwd), venv=self)

    def _run(
        self, *args: str, cwd: ty.Optional[Path] = None, input: ty.Optional[str] = None
    ) -> subprocess.CompletedProcess:
        return _subprocess_run([*args], self.cwd(cwd), venv=self, input=input)

    def run(
        self, *args: str, cwd: ty.Optional[Path] = None
    ) -> subprocess.CompletedProcess:
        return _subprocess_run([self.python, *args], self.cwd(cwd), venv=self)

    def run_module(
        self,
        entrypoint: str,
        *args: str,
        cwd: ty.Optional[Path] = None,
        input: ty.Optional[str] = None,
        env: ty.Optional[ty.Dict[str, str]] = None,
        print_command: bool = False,
        print_output: bool = False,
        popen_args: dict = {},
    ) -> subprocess.CompletedProcess:
        command = [self.python, "-m", entrypoint, *args]
        return _subprocess_run(
            command,
            self.cwd(cwd),
            input=input,
            env=env,
            venv=self,
            print_command=print_command,
            print_output=print_output,
            **popen_args,
        )

    @classmethod
    def cached(
        cls,
        package_name: str,
        build_venv: "Venv",
        cwd: ty.Optional[Path] = None,
        requirements: ty.Optional["RequirementSet"] = None,
    ) -> "Venv":
        venv_path = cls._get_venv_cache_path(package_name, mkdir=True)
        current_python_version = platform.python_version()
        try:
            venv = build_venv.create_or_activate_venv(
                venv_path, require_python_version=current_python_version
            )
        except (PythonVersionError, InvalidVenvError):
            shutil.rmtree(venv_path, ignore_errors=True)
            venv = build_venv.create_or_activate_venv(venv_path)

        if requirements:
            requirements_file = venv_path / "requirements.txt"
            cached_reqs = None
            if requirements_file.is_file():
                cached_reqs = RequirementSet.from_txt(requirements_file)
            if (
                cached_reqs is not None
                and cached_reqs != requirements
                or cached_reqs is None
            ):
                tmp_install = venv_path / "dependencies.txt"
                wheels = []
                # Split the installs into two parts:
                # 1. Non-wheel dependencies
                # 2. Local wheels (force reinstalled)
                tmp_install.write_text(
                    requirements.replace_local_wheel_links(
                        replace=lambda wheel_path: wheels.append(wheel_path)
                    ).to_txt()
                )
                # TODO:pip-sync with --python-executable pointing to venv python
                venv.install("-r", str(tmp_install.absolute()), no_deps=True)
                venv.install(
                    *[str(w.absolute()) for w in wheels],
                    no_deps=True,
                    force_reinstall=True,
                )
                requirements_file.write_text(requirements.to_txt())
                tmp_install.unlink()
        return venv


def wheel_file_to_version_pin(wheel_path: Path) -> Requirement:
    parsed = WheelName.from_filename(wheel_path.name)
    return Requirement(f"{parsed.name}=={str(parsed.version)}")


class RequirementSet:
    def __init__(self, requirements: ty.Iterable[ty.Union[Requirement, str]]) -> None:
        self._requirements = frozenset(
            [Requirement(r) if isinstance(r, str) else r for r in requirements]
        )

    def _validate(self, requirement: Requirement) -> None:
        if requirement.name is None:
            raise ValueError("Invalid requirement, must have a name")

    @cached_property
    def _by_name(self) -> ty.Dict[str, frozenset[Requirement]]:
        by_name = self.collect_by_name(self._requirements)
        return by_name

    def __iter__(self) -> ty.Iterator[Requirement]:
        return iter(sorted(self._requirements, key=lambda r: str(r)))

    def __len__(self) -> int:
        return len(self._requirements)

    def __contains__(self, item: ty.Any) -> bool:
        if isinstance(item, str):
            # item must be a distribution name
            return item in self._by_name
        elif isinstance(item, Requirement):
            # item is an exact requirement
            return item in self._requirements
        else:
            raise TypeError(f"Expected str or Requirement, got {type(item)}")

    def __getitem__(self, item: str) -> ty.Optional[frozenset[Requirement]]:
        return self._by_name.get(item, frozenset())

    def __repr__(self) -> str:
        return f"RequirementSet({list(self)})"

    def __eq__(self, other: ty.Any) -> bool:
        if not isinstance(other, RequirementSet):
            return NotImplemented
        return self._requirements == other._requirements

    def __hash__(self) -> int:
        return hash(self._requirements)

    @classmethod
    def collect_by_name(
        cls, *iterables: ty.Iterable[ty.Union[Requirement, str]]
    ) -> ty.Dict[str, frozenset[Requirement]]:
        by_name = defaultdict(set)
        for r in itertools.chain(*iterables):
            req = Requirement(r) if isinstance(r, str) else r
            by_name[req.name].add(req)
        return {k: frozenset(v) for k, v in by_name.items()}

    def partition(
        self, include: ty.Callable[[Requirement], bool]
    ) -> ty.Tuple["RequirementSet", "RequirementSet"]:
        included = []
        excluded = []
        for req in self:
            if include(req):
                included.append(req)
            else:
                excluded.append(req)
        return RequirementSet(included), RequirementSet(excluded)

    def merge(
        self, *others: ty.Iterable[ty.Union[str, Requirement]]
    ) -> "RequirementSet":
        return RequirementSet(itertools.chain(self, *others))

    def replace_local_wheel_links(
        self,
        wheels_to_replace: ty.Optional[ty.Set[str]] = None,
        replace: ty.Callable[
            [Path], ty.Optional[Requirement]
        ] = wheel_file_to_version_pin,
    ) -> "RequirementSet":
        def _should_replace(req: Requirement):
            name_matches = (
                wheels_to_replace is not None and req.name in wheels_to_replace
            )
            return (wheels_to_replace is None or name_matches) and _get_local_wheel_url(
                req
            ) is not None

        to_replace, keep = self.partition(_should_replace)
        replaced = []
        for req in to_replace:
            wheel_path = _get_local_wheel_url(req)
            assert (
                wheel_path is not None
            ), "expected local wheel to have a file:// url in compiled requirements file"
            replacement = replace(wheel_path)
            if replacement is not None:
                replaced.append(replacement)
        return keep.merge(replaced)

    @classmethod
    def from_txt(
        cls, txt: ty.Union[str, Path], ignore_comments: bool = True
    ) -> "RequirementSet":
        if isinstance(txt, Path):
            txt = txt.read_text()
        lines = txt.splitlines()
        lines = (line for line in lines if line.strip())
        if ignore_comments:
            lines = (line for line in lines if not line.lstrip().startswith("#"))

        return RequirementSet(lines)

    def to_txt(self) -> str:
        return "\n".join(str(req) for req in self)

    def to_lines(self) -> ty.List[str]:
        return [str(req) for req in self]


@dataclass
class WheelName:
    filename: str
    name: packaging.utils.NormalizedName
    version: str
    build: ty.Optional[ty.Tuple[int, str]]
    tags: ty.Set[packaging.tags.Tag]

    @classmethod
    def from_filename(cls, filename: str) -> "WheelName":
        name, version, build, tags = packaging.utils.parse_wheel_filename(filename)
        return cls(
            filename=filename,
            name=name,
            version=str(version),
            build=build if build else None,
            tags=set(tags),
        )


def _get_venvs_cache_path():
    cache_path = user_cache_dir(
        # the version key here should be updated if we make breaking changes to the cache contents
        appname="Prodigy Teams",
        appauthor="Explosion",
        version="0.1",
    )
    return Path(cache_path) / "venvs"


def _get_local_wheel_url(req: Requirement) -> ty.Optional[Path]:
    if req.url is not None and req.url.startswith("file://"):
        url_path = Path(req.url.replace("file://", ""))
        if url_path.suffix == ".whl":
            return url_path
    return None


def _utf8_decode(b: bytes) -> str:
    return b.decode()


def _source_sh(
    activate_path: Path,
    *,
    env: ty.Optional[ty.Dict[str, str]] = None,
    cwd: Path,
    decode_key=_utf8_decode,
    decode_value=_utf8_decode,
) -> ty.Dict[str, str]:
    cmd = f". {shlex.quote(str(activate_path.absolute()))}; env -0"
    ret = subprocess.run(
        cmd,
        shell=True,
        check=True,
        capture_output=True,
        env=env,
    )
    result = {}
    kvs = [line.partition(b"=")[::2] for line in ret.stdout.split(b"\0")]
    result.update((decode_key(k), decode_value(v)) for k, v in kvs)
    return result


def _subprocess_run(
    args: ty.List[str],
    cwd: Path,
    input: ty.Optional[str] = None,
    env: ty.Optional[ty.Dict[str, str]] = None,
    venv: ty.Optional[Venv] = None,
    print_command: bool = False,
    print_output: bool = False,
    popen_args: dict = {},
) -> subprocess.CompletedProcess:
    if env is None:
        env = os.environ.copy()

    if venv and venv.activate_script is not None:
        venv_config = _source_sh(venv.activate_script, cwd=cwd, env=env)
        for k in ["PATH", "VIRTUAL_ENV", "PYTHONHOME", "VIRTUAL_ENV_PROMPT"]:
            if k in venv_config:
                env[k] = venv_config[k]
            elif k in env:
                del env[k]

    if print_command:
        print(shlex.join(args), file=sys.stderr)
    try:
        ret = subprocess.run(
            args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            text=True,
            input=input,
            encoding="utf8",
            env=env,
            **popen_args,
        )
    except subprocess.CalledProcessError as e:
        print(e.output, file=sys.stderr)
        raise
    if print_output:
        print(ret.stdout, file=sys.stderr)
    return ret


@contextmanager
def _make_tempdir() -> ty.Generator[Path, None, None]:
    """Execute a block in a temporary directory and remove the directory and
    its contents at the end of the with block.

    YIELDS (Path): The path of the temp directory.
    """
    d = Path(tempfile.mkdtemp())
    yield d
    shutil.rmtree(str(d))
