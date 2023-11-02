"""Commands for merging PRs."""
import sys

import typer
from rich import print  # noqa: W0622

from dapla_team_cli.pr.merge.merge_all import merge_all
from dapla_team_cli.pr.state.state_utils import state_object_handler


def merge(
    override: bool = typer.Option(
        False, "--override", "-o", help="Yields an option to merge PRs that the state file records as having already been merged"
    ),
) -> None:
    """Merges all pull requests."""
    if state := state_object_handler.get_user_state():
        merge_all(state, override)
    else:
        sys.exit(1)
    print("\n[yellow]Hint: You can use 'dpteam pr state show' to get a table of all the PR states")
