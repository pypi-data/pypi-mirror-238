"""Module for generating state file."""

import subprocess  # noqa: S404 unnecessary warning ref: https://github.com/PyCQA/bandit/issues/455
from pathlib import Path
from typing import Optional
from typing import Union

import questionary
from rich import print  # noqa: W0622

from dapla_team_cli.pr.const import STATE_BUCKET_NAME_URI
from dapla_team_cli.pr.const import PrMetadata
from dapla_team_cli.pr.const import RepoState
from dapla_team_cli.pr.const import State
from dapla_team_cli.pr.const import WorkflowStatus
from dapla_team_cli.pr.state.state_utils import state_object_handler


def generate(state_name: Optional[str] = None, folder_path: Optional[Path] = None) -> None:
    """Generates a new statefile."""
    result = subprocess.run(
        ["gcloud", "config", "list", "account", "--format", "value(core.account)"], stdout=subprocess.PIPE, check=True
    )  # noqa
    # Decode the output from bytes to a string
    run_invoker = result.stdout.decode().strip().replace("@ssb.no", "")

    if not state_name:
        run_name_prompt = questionary.text(
            f"What do you want to call this run? It will be called 'batch-{run_invoker}-[your-input]. Run name:'"
        ).ask()
        state_name = f"batch-{run_invoker}-{run_name_prompt}"

    if folder_path is None:
        folder_path = questionary.path(
            "What's the path to the root folder of the repos to be updated?", only_directories=True
        ).ask()
    state: State = _generate_state_data_from_path(folder_path, state_name)
    state_object_handler.set_state(state)
    print(f"\n[green]✅ state file {state_name} created and uploaded to {STATE_BUCKET_NAME_URI}")


def _generate_state_data_from_path(path: Union[str, Path], state_name: str) -> State:
    """Helper function to generate state file from local files."""
    root_path: Path = Path(path).absolute()
    repos = {}
    dot_git = ".git"
    for folder in root_path.iterdir():
        # We're interested in directories containing a .git file i.e. repositories
        if folder.is_dir() and folder / dot_git in folder.rglob(dot_git):
            # Create an entry in state so we can track this repo
            repos[folder.name] = RepoState(name=folder.name, local_path=folder, pr=PrMetadata(), workflow=WorkflowStatus())

    return State(name=state_name, repos=repos)
