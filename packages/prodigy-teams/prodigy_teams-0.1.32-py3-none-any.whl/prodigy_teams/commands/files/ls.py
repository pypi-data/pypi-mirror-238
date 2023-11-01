from radicli import Arg
from wasabi import msg

from ... import ty
from ...cli import cli
from ...errors import CLIError
from ...messages import Messages
from ...prodigy_teams_broker_sdk import models as broker_models
from ...ui import print_as_json
from ...util import _resolve_broker_ref, _resolve_remote_path, collapse_path_aliases
from .._state import get_auth_state, get_saved_settings


@cli.subcommand(
    "files",
    "ls",
    remote=Arg(help=Messages.remote_path),
    recurse=Arg("--recurse", "-r", help=Messages.recurse_list),
    as_json=Arg("--json", help=Messages.as_json),
    cluster_host=Arg("--cluster-host", help=Messages.cluster_host),
    expand_remote_paths=Arg(
        "--expand-path-aliases", help=Messages.files_expand_path_alias
    ),
)
def ls(
    remote: str,
    recurse: bool = False,
    as_json: bool = False,
    cluster_host: ty.Optional[str] = None,
    expand_remote_paths: bool = False,
) -> broker_models.PathList:
    """List the files under `remote`"""
    settings = get_saved_settings()
    auth = get_auth_state()
    broker_host = _resolve_broker_ref(auth.client, cluster_host or settings.broker_host)
    remote_root, subpath, full_remote_path = _resolve_remote_path(
        auth.client, remote, str(broker_host)
    )
    body = broker_models.Listing(
        path=full_remote_path, recurse=recurse, include_stats=False
    )
    files = auth.broker_client.files.list_dir(body)
    if not files.exists:
        raise CLIError(
            Messages.E054.format(path_input=remote, resolved_path=full_remote_path)
        )
    if remote_root and not expand_remote_paths:
        aliases = {remote_root.name: remote_root.path}
        files.paths = [collapse_path_aliases(p, aliases) for p in files.paths]
    if not files.paths:
        if recurse:
            msg.info(Messages.T049.format(path_input=remote))
        else:
            msg.info(Messages.T050.format(path_input=remote))
    if as_json:
        print_as_json(files.dict())
    else:
        for file_path in files.paths:
            print(file_path)
    return files
