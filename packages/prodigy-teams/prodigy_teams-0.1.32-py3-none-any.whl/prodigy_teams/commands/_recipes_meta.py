"""Generate a wheel for a prodigy_teams_recipes package,
including updating its meta file and requirements files."""
import json
import os
import re
import shlex
import shutil
import subprocess
from contextlib import ExitStack
from functools import cached_property
from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version

from prodigy_teams.errors import RecipeBuildMetaFailed

from .. import ty
from ..build import (
    DirectorySource,
    RequirementSet,
    Venv,
    WheelSource,
    _get_venvs_cache_path,
    _make_tempdir,
)

RecipeInput = ty.Union[Requirement, WheelSource, DirectorySource]
ExtraWheelsInput = ty.Union[WheelSource, DirectorySource]


class RecipeBuilder:
    def __init__(
        self,
        src: RecipeInput,
        extras: ty.List[ExtraWheelsInput],
        wheelhouse: ty.Optional[Path] = None,
        build_dir: ty.Optional[Path] = None,
        cwd: ty.Optional[Path] = None,
        clear_cache: bool = False,
        target_python_version: ty.Optional[str] = None,
        target_platform: ty.Optional[str] = None,
        target_implementation: ty.Optional[str] = None,
        cache_pip_compile: bool = True,
    ):
        if clear_cache:
            venvs_cache = _get_venvs_cache_path()
            if venvs_cache.exists:
                shutil.rmtree(venvs_cache, ignore_errors=True)
        self._clear_cache = clear_cache
        self._cache_pip_compile = cache_pip_compile
        self._exit_stack = ExitStack()
        if build_dir is not None:
            self.build_dir = build_dir
        else:
            self.build_dir = self._exit_stack.enter_context(_make_tempdir())

        self.recipe_distribution_name = (
            src.name if isinstance(src, Requirement) else src.distribution_name
        )
        self.src = src
        self.extras = extras
        if wheelhouse is not None:
            self.wheelhouse = wheelhouse
        else:
            self.wheelhouse = self._exit_stack.enter_context(_make_tempdir())
        self._cwd = cwd
        self._upgrade_builder_venv = False
        self._target_python_version = target_python_version
        self._target_platform = target_platform
        self._target_implementation = target_implementation
        self._init_build_dir()

    def __enter__(self) -> "RecipeBuilder":
        return self

    def __exit__(self, _exc_type, _exc, _exc_tb):
        self._exit_stack.close()

    @cached_property
    def _builder_env_requirements(self) -> RequirementSet:
        return RequirementSet(
            ["setuptools==65.4.1", "wheel", "pip-tools>=6.13.0", "pip", "build>=0.10.0"]
        )

    @cached_property
    def _builder_venv(self) -> "Venv":
        with Venv.from_active(cwd=self._cwd) as venv:
            _builder_venv = Venv.cached(
                "__prodigy_teams__",
                build_venv=venv,
            )
            _builder_venv.install(
                *self._builder_env_requirements.to_lines(), upgrade=False
            )
        return _builder_venv

    @cached_property
    def recipe_version(self) -> Version:
        if isinstance(self.src, Requirement):
            version_spec = self.src.specifier
            if len(version_spec) == 1 and all(
                s.operator == "==" and s.version for s in version_spec
            ):
                return Version(next(iter(version_spec)).version)
            else:
                return self.prepared_wheelhouse[self.recipe_distribution_name].version
        elif isinstance(self.src, DirectorySource) and self.src.version is not None:
            return self.src.version
        else:
            return self.prepared_wheelhouse[self.recipe_distribution_name].version

    @cached_property
    def recipe_wheel(self) -> WheelSource:
        if isinstance(self.src, (Requirement, DirectorySource)):
            return self.prepared_wheelhouse[self.recipe_distribution_name]
        else:
            return self.src

    @cached_property
    def recipe_package_name(self) -> str:
        if isinstance(self.src, (Requirement, DirectorySource)):
            return self.prepared_wheelhouse[self.recipe_distribution_name].package_name
        else:
            return self.src.package_name

    @cached_property
    def resolved_input_requirements(self) -> RequirementSet:
        """
        Resolve the versions of the input packages.
        """
        requirements = set()
        for pkg in [self.src, *self.extras]:
            if isinstance(pkg, Requirement):
                requirements.add(pkg)
            elif pkg.version is not None:
                # requirements.add(Requirement(f"{pkg.distribution_name}=={pkg.version}"))
                requirements.add(Requirement(f"{pkg.distribution_name}=={pkg.version}"))
            else:
                # we need to build the wheel (metadata) to figure out the version
                built_wheels = self.prepared_wheelhouse
                wheel = built_wheels[pkg.distribution_name]
                requirements.add(
                    Requirement(f"{wheel.distribution_name}=={wheel.version}")
                )
        return RequirementSet(requirements)

    def _init_build_dir(self):
        local_requirements = self.build_dir / "recipe_requirements.txt"
        if self._cache_pip_compile:
            cached_venv = Venv._get_venv_cache_path(
                self.recipe_distribution_name, mkdir=False
            )
            cached_reqs = cached_venv / "requirements.txt"
            if cached_reqs.is_file():
                local_requirements.write_text(cached_reqs.read_text())

    @cached_property
    def compiled_venv_requirements(
        self,
    ) -> ty.Tuple[Path, Path, ty.List[str]]:
        local_reqs_file = self.build_dir / "recipe_requirements.txt"
        # cloud_reqs_file = self.build_dir / "cloud_requirements.txt"
        requirements = []
        if isinstance(self.src, Requirement):
            requirements.append(self.src)
        requirements.extend(self.prepared_wheelhouse.values())
        upgrade_packages = [r.name for r in self.resolved_input_requirements]
        compile_requirements(
            self._builder_venv,
            requirements=requirements,
            wheelhouse=self.wheelhouse,
            output_path=local_reqs_file,
            # upgrade_packages=upgrade_packages,
            upgrade=True,
            pip_tools_cache=self._get_pip_tools_cache(),
        )
        # Cross-compiling requirements is not supported by pip-compile
        # https://github.com/jazzband/pip-tools/pull/
        # compile_requirements(
        #     self._builder_venv,
        #     requirements=requirements,
        #     wheelhouse=self.wheelhouse,
        #     output_path=cloud_reqs_file,
        #     # upgrade_packages=upgrade_packages,
        #     upgrade=True,
        #     pip_tools_cache=self._get_pip_tools_cache(),
        #     python_version=self._target_python_version,
        #     python_platform=self._target_platform,
        #     python_implementation=self._target_implementation,
        # )
        return (
            local_reqs_file,
            local_reqs_file,
            upgrade_packages,
        )

    @cached_property
    def recipe_requirements_local(self) -> RequirementSet:
        reqs_file, _, _ = self.compiled_venv_requirements
        return RequirementSet.from_txt(reqs_file.read_text())

    @cached_property
    def recipes_venv(
        self,
    ) -> "Venv":
        recipes_venv = Venv.cached(
            self.recipe_distribution_name,
            self._builder_venv,
            requirements=self.recipe_requirements_local,
        )
        return recipes_venv

    @cached_property
    def prepared_wheelhouse(self) -> ty.Dict[str, WheelSource]:
        """
        Builds all local dependencies, and returns a mapping from distribution name to wheels.
        """
        wheels = []
        to_build = []
        for src in [self.src, *self.extras]:
            if isinstance(src, WheelSource):
                wheels.append(src)
            elif isinstance(src, DirectorySource):
                to_build.append(src)
            else:
                requirements = self.recipe_requirements_local
                requirements[self.recipe_distribution_name]
        wheels.extend(
            self._build_wheels(
                [p.path for p in to_build], self.wheelhouse, no_deps=True
            )
        )
        return {w.distribution_name: w for w in wheels}

    def _build_wheels(
        self,
        srcs: ty.List[Path],
        dest: Path,
        no_deps: bool = False,
        find_links: ty.List[Path] = [],
        cwd: ty.Optional[Path] = None,
    ) -> ty.List[WheelSource]:
        pip_wheel_args = [*[str(p.resolve()) for p in srcs], "-w", str(dest.absolute())]
        if no_deps:
            pip_wheel_args.append("--no-deps")
        if find_links:
            for dir in find_links:
                pip_wheel_args.extend(["-f", str(dir)])
        # SKIP_CYTHON is used here to ensure the prodigy wheel is platform independent.
        # - In the long run we need a better solution since this only works for optional
        #   native dependencies
        result = self._builder_venv.run_module(
            "pip",
            "wheel",
            *pip_wheel_args,
            cwd=cwd,
            env=dict(os.environ, SKIP_CYTHON="1"),
        )
        wheels = re.findall(r"(?<=filename=)\S+", result.stdout)
        return [WheelSource((dest / wheel).absolute()) for wheel in wheels]

    def _get_depcache(self) -> ty.List[Path]:
        pip_tools_cache = self._get_pip_tools_cache()
        return [p for p in pip_tools_cache.glob("depcache-cp*.json")]

    def _get_pip_tools_cache(self) -> Path:
        venv_cache = self._builder_venv._get_venv_cache_path(
            "__prodigy_teams__", mkdir=True
        )
        pip_tools_cache = venv_cache / "pip-tools-cache"
        pip_tools_cache.mkdir(exist_ok=True)
        return pip_tools_cache

    def _recipe_venv_path(self) -> Path:
        return self._builder_venv._get_venv_cache_path(
            self.recipe_distribution_name, mkdir=True
        )

    @cached_property
    def recipes_meta(
        self,
    ) -> ty.Dict[str, ty.Any]:
        recipes_venv = self.recipes_venv
        wheels = self.prepared_wheelhouse
        _, cloud_reqs_path, _ = self.compiled_venv_requirements
        cleaned_requirements = RequirementSet.from_txt(
            cloud_reqs_path
        ).replace_local_wheel_links(set(wheels.keys()))

        try:
            recipes_meta = json.loads(
                recipes_venv.run_module(
                    "prodigy_teams_recipes_sdk", "create-meta", self.recipe_package_name
                ).stdout
            )
        except subprocess.CalledProcessError as e:
            raise RecipeBuildMetaFailed(
                self.recipe_package_name, stdout=e.stdout, stderr=e.stderr
            )

        pkg_meta = self.recipe_wheel.pkginfo_metadata
        meta = {
            "name": self.recipe_wheel.distribution_name,
            "version": str(self.recipe_wheel.version),
            "description": pkg_meta.summary if pkg_meta is not None else None,
            "author": pkg_meta.author if pkg_meta is not None else None,
            "email": pkg_meta.author_email if pkg_meta is not None else None,
            "url": pkg_meta.home_page if pkg_meta is not None else None,
            "license": pkg_meta.license if pkg_meta is not None else None,
            "assets": {},
            "recipes": recipes_meta,
            "requirements": cleaned_requirements.to_lines(),
        }
        # Check it's json serializable
        _ = json.dumps(meta, indent=2)
        return meta


def compile_requirements(
    venv: Venv,
    requirements: ty.List[ty.Union[Requirement, WheelSource, str]],
    wheelhouse: Path,
    output_path: Path,
    pip_tools_cache: Path,
    upgrade_packages: ty.Iterable[str] = [],
    upgrade: bool = False,
    python_version: ty.Optional[str] = None,
    python_platform: ty.Optional[str] = None,
    python_implementation: ty.Optional[str] = None,
):
    # def collect_wheel_files(wheels: ty.List[WheelSource], wheelhouse: Path):
    #     """
    #     Get all of the local wheels we want to include so we can check
    #     if their requirements changed without a version change.
    #     """
    #     # TODO: this assumes the wheelhouse only includes the wheels we need
    #     # we should expand from the requirements in the initial wheels set
    #     # or send in the full set of wheels to be included
    #     all_wheels = {w.distribution_name: w for w in wheels}
    #     for wheel_path in wheelhouse.iterdir():
    #         if wheel_path.suffix == ".whl":
    #             wheel = WheelSource(wheel_path)
    #             if wheel.distribution_name not in all_wheels:
    #                 all_wheels[wheel.distribution_name] = wheel
    #             else:
    #                 # sanity check incase the wheelhouse contains multiple versions
    #                 assert (
    #                     all_wheels[wheel.distribution_name].version == wheel.version
    #                 ), f"Multiple versions of {wheel.distribution_name} found in wheelhouse (not implemented)"
    #     return all_wheels

    def refresh_pip_tools_cache(
        pip_tools_cache: Path, all_wheels: ty.Dict[str, WheelSource]
    ) -> Path:
        """
        Initializes the pip-compile cache, ensuring that the cache is not stale
        for any of the provided wheels.
        """
        for cache_file in pip_tools_cache.glob("depcache-cp*.json"):
            if not cache_file.is_file():
                continue

            cache = json.loads(cache_file.read_text())
            packages_to_refresh = {}

            for name, versions in cache.get("dependencies", {}).items():
                if (
                    name not in all_wheels
                    or str(all_wheels[name].version) not in versions
                ):
                    continue
                wheel = all_wheels[name]
                cached_reqs = versions.get(str(wheel.version), None)
                if set(Requirement(r) for r in cached_reqs) != wheel.requirements:
                    packages_to_refresh[(name, wheel.version)] = wheel.requirements

            if packages_to_refresh:
                for (name, version), requirements in packages_to_refresh.items():
                    package_cache = cache.setdefault("dependencies", {}).setdefault(
                        name, {}
                    )
                    if requirements is not None:
                        package_cache[str(version)] = [str(r) for r in requirements]
                    elif str(version) in package_cache:
                        del package_cache[str(version)]
                cache_file.write_text(json.dumps(cache))
        return pip_tools_cache

    wheels = []
    specs = []

    pip_args = []

    for req in requirements:
        if isinstance(req, WheelSource):
            wheels.append(req)
            wheel_path = req.path.resolve().as_uri()
            specs.append(f"{req.distribution_name} @ {wheel_path}")
        elif isinstance(req, str):
            specs.append(str(Requirement(req)))
        else:
            specs.append(str(req))

    if pip_tools_cache:
        refresh_pip_tools_cache(
            pip_tools_cache, {w.distribution_name: w for w in wheels}
        )
        cache_flag = ["--cache-dir", str(pip_tools_cache.resolve())]
    else:
        cache_flag = ["--rebuild"]

    upgrade_packages = list(
        set(upgrade_packages).union([w.distribution_name for w in wheels])
    )
    upgrade_packages_args = []
    if upgrade:
        upgrade_packages_args = ["--upgrade"]
    else:
        for to_upgrade in upgrade_packages:
            upgrade_packages_args.extend(["-P", to_upgrade])

    if python_version is not None:
        pip_args.extend(["--python-version", python_version])
    if python_platform is not None:
        pip_args.extend(["--platform", python_platform])
    if python_implementation is not None:
        pip_args.extend(["--implementation", python_implementation])

    return venv.run_module(
        "piptools",
        "compile",
        "-",  # read specs from stdin
        "--output-file",
        str(output_path.resolve()),
        "-f",
        str(wheelhouse.absolute()),
        "--no-emit-find-links",
        *cache_flag,
        *(["--pip-args", shlex.join(pip_args)] if pip_args else []),
        *upgrade_packages_args,
        input="\n".join(specs),
    )
