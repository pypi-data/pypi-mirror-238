import functools
import posixpath
from pathlib import Path, PurePosixPath

from radicli import Arg
from wasabi import msg

from ... import ty
from ...cli import cli
from ...errors import BrokerError, CLIError
from ...messages import Messages
from ...prodigy_teams_broker_sdk import Client as BrokerClient
from ...prodigy_teams_broker_sdk import models as broker_models
from ...ui import Progress, is_silent
from ...util import _is_root_path, _resolve_broker_ref, is_local, resolve_remote_path
from .._state import get_auth_state, get_saved_settings


class CopyCallable(ty.Protocol):
    def __call__(
        self,
        *,
        src: str,
        dest: str,
        overwrite: bool,
        recurse: bool,
        make_dirs: bool,
        broker_client: BrokerClient,
    ) -> ty.Optional[str]:
        ...


@cli.subcommand(
    "files",
    "cp",
    src=Arg(help=Messages.remote_local_path.format(noun="source")),
    dest=Arg(help=Messages.remote_local_path.format(noun="destination")),
    recurse=Arg("--recurse", "-r", help=Messages.recurse_copy),
    make_dirs=Arg("--make-dirs", help=Messages.make_dirs),
    overwrite=Arg("--overwrite", help=Messages.overwrite),
    cluster_host=Arg("--cluster-host", help=Messages.cluster_host),
)
def cp(
    src: str,
    dest: str,
    recurse: bool = False,
    make_dirs: bool = False,
    overwrite: bool = False,
    cluster_host: ty.Optional[str] = None,
) -> None:
    """Copy files to and from the cluster"""
    settings = get_saved_settings()
    auth = get_auth_state()
    broker_host = str(
        _resolve_broker_ref(auth.client, cluster_host or settings.broker_host)
    )
    is_src_local = is_local(src)
    is_dest_local = is_local(dest)

    def _cp(f: CopyCallable, *, src: str, dest: str) -> ty.Optional[str]:
        return f(
            src=src,
            dest=dest,
            overwrite=overwrite,
            recurse=recurse,
            make_dirs=make_dirs,
            broker_client=auth.broker_client,
        )

    if is_src_local and is_dest_local:  # both local
        raise CLIError(Messages.E015.format(verb="copy"), f"{src}, {dest}")
    elif is_src_local and not is_dest_local:  # from local to remote
        err = _cp(
            _upload,
            src=src,
            dest=resolve_remote_path(auth.client, dest, broker_host),
        )
    elif not is_src_local and is_dest_local:
        # From remote to local
        err = _cp(
            _download,
            src=resolve_remote_path(auth.client, src, broker_host),
            dest=dest,
        )
    else:
        # Both remote
        err = _cp(
            _copy_on_remote,
            src=resolve_remote_path(auth.client, src, broker_host),
            dest=resolve_remote_path(auth.client, dest, broker_host),
        )
    if err is not None:
        raise CLIError(err)
    elif not is_silent():
        msg.good(Messages.T011, f"{src} -> {dest}")


def _upload(
    *,
    src: str,
    dest: str,
    make_dirs: bool,
    overwrite: bool,
    recurse: bool,
    broker_client: BrokerClient,
) -> ty.Optional[str]:
    src_has_trailing_slash = src.endswith("/")
    src_path = Path(src)
    src_base = src

    @functools.lru_cache()
    def _ls(remote_path: str):
        try:
            files = broker_client.files.list_dir(
                broker_models.Listing(
                    path=remote_path, recurse=False, include_stats=False
                )
            )
            return files
        except BrokerError as e:
            raise CLIError(Messages.E018, e)

    src_exists = src_path.exists()
    src_is_file = src_path.is_file()
    src_is_dir = src_path.is_dir()

    dest_exists = _ls(dest).exists
    dest_is_file = _ls(dest).is_file
    dest_is_dir = dest_exists and not dest_is_file

    # print(
    #     f"""
    # _upload({src=},{dest=}):
    #            {_ls(dest).paths=}
    #            {src_is_file=}
    #            {src_is_dir=}
    #            {src_has_trailing_slash=}
    #
    #            {dest_exists=}
    #            {dest_is_dir=}
    #            {dest_is_file=}
    # """.strip(),
    #     file=sys.stderr,
    # )

    if not src_exists:
        raise CLIError("No such file or directory", src)

    if src_is_dir and not recurse:
        raise CLIError(Messages.E016.format(verb="upload"), src_path)

    if dest_is_file:
        if src_is_file and not overwrite:
            raise CLIError("The destination file already exists and overwrite is False")
        elif src_is_dir:
            raise CLIError("A file already exists at the destination path")

    if src_is_file:
        src_file = src_path
        if dest_is_file:
            dest_file = dest
        elif dest_is_dir or dest.endswith("/"):
            dest_file = posixpath.join(dest, src_path.name)
        else:
            dest_file = dest
        dest_base = posixpath.dirname(dest_file)
        create_base = False
        paths = [(src_file, dest_file)]
    else:
        if dest_is_dir and src_has_trailing_slash:
            # `cp src/ dest_exists/` copies `src/**` into `dest_exists/**`
            dest_base = dest
            create_base = False
        elif dest_is_dir and not src_has_trailing_slash:
            # `cp src dest_exists/` copies `src/**` into `dest_exists/src/**`
            dest_base = posixpath.join(dest, src_path.name)
            create_base = True
        else:
            # `cp src dest_noexists/` copies `src/**` into `dest_noexists/**`
            create_base = True
            dest_base = dest
        src_base = src_path

        paths = [
            (
                Path(src_file),
                posixpath.join(
                    dest_base, str(PurePosixPath(src_file.relative_to(src_base)))
                ),
            )
            for src_file in src_path.glob("**/*")
        ]

    if not make_dirs and not _is_root_path(dest_base):
        # we can't precreate empty dirs on cloud paths, but we can
        # override the make_dirs flag to create the appropriate dirs on demand
        # if we first check the existence of the parent dirs
        required_parent = posixpath.dirname(dest_base) if create_base else dest_base

        parent_ls = _ls(required_parent)

        # print(
        #     f"""
        #        {required_parent=}
        #        {parent_ls.exists=}
        #        {parent_ls.is_file=}
        #        {create_base=}
        # """.rstrip(),
        #     file=sys.stderr,
        # )
        if parent_ls.exists and not parent_ls.is_file:
            make_dirs = True
        elif parent_ls.is_file:
            raise CLIError(
                "A file already exists at the destination path", required_parent
            )
        else:
            raise CLIError(Messages.E021, dest_base)

    #     print(
    #         f"""
    #                {paths=}
    # """.rstrip(),
    #         file=sys.stderr,
    #     )
    with Progress(paths) as paths:
        for src_file, dest_file in paths:
            if src_file.is_dir():
                continue
            body = src_file.open("rb")
            try:
                broker_client.files.upload(
                    body, dest=dest_file, overwrite=overwrite, make_dirs=make_dirs
                )
            except BrokerError as e:
                raise CLIError(Messages.E017.format(verb="upload"), e)


def _download(
    *,
    src: str,
    dest: ty.Union[str, Path],
    make_dirs: bool,
    overwrite: bool,
    recurse: bool,
    broker_client: BrokerClient,
    verbose: bool = False,
) -> ty.Optional[str]:
    dest = Path(dest)
    body = broker_models.Listing(path=src, recurse=recurse, include_stats=False)
    try:
        files = broker_client.files.list_dir(body)
    except BrokerError as e:
        raise CLIError(Messages.E018, e)

    src_exists = files.exists
    src_is_file = files.is_file
    src_is_dir = src_exists and not src_is_file
    src_has_trailing_slash = src.endswith("/")

    dest_is_dir = dest.is_dir()
    dest_is_file = dest.is_file()

    #     print(
    #         f"""
    # _download({src=},{dest=}):
    #            {files.paths=}
    #            {src_is_file=}
    #            {src_is_dir=}
    #            {src_has_trailing_slash=}
    #
    #            {dest_exists=}
    #            {dest_is_dir=}
    #            {dest_is_file=}
    # """.strip()
    #     file=sys.stderr,
    #     )

    if not src_exists and not files.paths:
        raise CLIError("No such file or directory", src)

    if dest_is_file:
        if src_is_file and not overwrite:
            raise CLIError(Messages.E020, dest)
        elif src_is_dir:
            raise CLIError("A file already exists at the destination path")

    if src_is_dir and not recurse:
        raise CLIError(Messages.E016.format(verb="download"), src)

    if src_is_file:
        assert len(files.paths) == 1
        src_file = files.paths[0]
        if dest_is_file:
            dest_file = dest
        elif dest_is_dir:
            dest_file = dest / posixpath.basename(src_file)
        else:
            dest_file = dest
        dest_base = dest_file.parent
        create_base = False
        paths = [(src_file, dest_file)]
    else:
        if dest_is_dir and src_has_trailing_slash:
            # `cp src/ dest_exists/` copies `src/**` into `dest_exists/**`
            dest_base = dest
            create_base = False
        elif dest_is_dir and not src_has_trailing_slash:
            # `cp src dest_exists/` copies `src/**` into `dest_exists/src/**`
            dest_base = dest / posixpath.basename(src)
            create_base = True
        else:
            # `cp src dest_noexists/` copies `src/**` into `dest_noexists/**`
            create_base = True
            dest_base = dest
        src_base = src

        paths = [
            (src_file, dest_base / posixpath.relpath(src_file, src_base))
            for src_file in files.paths
        ]

    if not dest_base.is_dir():
        if make_dirs:
            dest_base.parent.mkdir(exist_ok=True, parents=True)
        elif create_base:
            dest_base.mkdir(exist_ok=True)
        else:
            raise CLIError(Messages.E021, dest_base)
    #     print(
    #         f"""
    #            {paths=}
    # """.strip()
    #     )

    with Progress(paths) as paths:
        for src_file, dest_file in paths:
            # Determine local destination for this file
            if dest_file.exists() and not overwrite:
                # We should only reach this check for recursive copies, so
                # rather than fail halfway through we just warn
                msg.warn(f"{dest_file} exists, skipping...")
                continue
            body = broker_models.Downloading(target=src_file)
            try:
                content = broker_client.files.download(body)
            except BrokerError as e:
                raise CLIError(Messages.E017.format(verb="download"), e)

            # Save content to local file
            dest_file.parent.mkdir(exist_ok=True, parents=True)
            if verbose:
                msg.info(f"writing {src_file} -> {dest_file}")
            with open(dest_file, "wb") as f:
                f.write(content.read())


def _copy_on_remote(
    *,
    src: str,
    dest: str,
    make_dirs: bool,
    overwrite: bool,
    recurse: bool,
    broker_client: BrokerClient,
) -> ty.Optional[str]:
    if recurse:
        body = broker_models.Copying(
            src=src, dest=dest, make_dirs=make_dirs, overwrite=overwrite
        )
        try:
            plan = broker_client.files.plan_directory_copy(body)
        except BrokerError as e:
            raise CLIError(Messages.E022, e)
        copies = plan.copy_
    else:
        copies = [
            broker_models.Copying(
                src=src, dest=dest, make_dirs=make_dirs, overwrite=overwrite
            )
        ]
    with Progress(copies) as copies:
        for file_copy_plan in copies:
            body = broker_models.Copying(
                src=file_copy_plan.src,
                dest=file_copy_plan.dest,
                make_dirs=make_dirs,
                overwrite=overwrite,
            )
            try:
                broker_client.files.copy(body)
            except BrokerError as e:
                raise CLIError(Messages.E017.format(verb="copy"), e)
