import io
import os
import sys
import tarfile
from pathlib import Path

import click
import requests

from tecton import tecton_context
from tecton._internals import metadata_service
from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli.command import TectonCommand
from tecton_core import repo_file_handler
from tecton_proto.metadataservice import metadata_service_pb2


def init_feature_repo() -> None:
    if Path().resolve() == Path.home():
        printer.safe_print("You cannot set feature repository root to the home directory", file=sys.stderr)
        sys.exit(1)

    # If .tecton exists in a parent or child directory, error out.
    repo_root = repo_file_handler._maybe_get_repo_root()
    if repo_root not in [Path().resolve(), None]:
        printer.safe_print(".tecton already exists in a parent directory:", repo_root)
        sys.exit(1)

    child_dir_matches = list(Path().rglob("*/.tecton"))
    if len(child_dir_matches) > 0:
        dirs_str = "\n\t".join((str(c.parent.resolve()) for c in child_dir_matches))
        printer.safe_print(f".tecton already exists in child directories:\n\t{dirs_str}")
        sys.exit(1)

    dot_tecton = Path(".tecton")
    if not dot_tecton.exists():
        dot_tecton.touch()
        printer.safe_print("Local feature repository root set to", Path().resolve(), "\n", file=sys.stderr)
        printer.safe_print("💡 We recommend tracking this file in git:", Path(".tecton").resolve(), file=sys.stderr)
        printer.safe_print(
            "💡 Run `tecton apply` to apply the feature repository to the Tecton cluster.", file=sys.stderr
        )
    else:
        printer.safe_print("Feature repository is already set to", Path().resolve(), file=sys.stderr)


@click.command(uses_workspace=True, cls=TectonCommand)
@click.argument("commit_id", required=False)
def restore(commit_id):
    """Restore feature repo state to that of past `tecton apply`.
    The commit to restore can either be passed as COMMIT_ID, or the latest will be used.
    """
    # Get the repo download URL from the metadata service.
    request = metadata_service_pb2.GetRestoreInfoRequest(workspace=tecton_context.get_current_workspace())
    if commit_id:
        request.commit_id = commit_id
    response = metadata_service.instance().GetRestoreInfo(request)

    # Download the repo.
    url = response.signed_url_for_repo_download
    commit_id = response.commit_id
    sdk_version = response.sdk_version
    # TODO: always print this message once enough customers are on new sdk versions
    sdk_version_msg = f"applied by SDK version {sdk_version}" if sdk_version else ""
    printer.safe_print(f"Restoring from commit {commit_id} {sdk_version_msg}")
    try:
        tar_response = requests.get(url)
        tar_response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(e)

    # Find the repo root or initialize a default repot if not in a repo.
    root = repo_file_handler._maybe_get_repo_root()
    if not root:
        init_feature_repo()
        root = Path().resolve()
    repo_file_handler.ensure_prepare_repo()

    # Get user confirmation.
    repo_files = repo_file_handler.repo_files()
    if len(repo_files) > 0:
        for f in repo_files:
            printer.safe_print(f)
        cli_utils.confirm_or_exit("This operation may delete or modify the above files. Ok?")
        for f in repo_files:
            os.remove(f)

    # Extract the feature repo.
    with tarfile.open(fileobj=io.BytesIO(tar_response.content), mode="r|gz") as tar:
        for entry in tar:
            if os.path.isabs(entry.name) or ".." in entry.name:
                msg = "Illegal tar archive entry"
                raise ValueError(msg)
            elif os.path.exists(root / Path(entry.name)):
                msg = f"tecton restore would overwrite an unexpected file: {entry.name}"
                raise ValueError(msg)
            tar.extract(entry, path=root)
    printer.safe_print("Success")


@click.command(requires_auth=False, cls=TectonCommand)
def init() -> None:
    """Initialize feature repo."""
    init_feature_repo()
