"""Deploy infrastructure changes by commenting 'atlantis apply' on PRs."""
import sys

import typer
from rich import print  # noqa: W0622

from dapla_team_cli.pr.atlantis_apply.atlantis_apply_all import atlantis_apply
from dapla_team_cli.pr.state.state_utils import state_object_handler


def apply(max_prs: int = typer.Argument(sys.maxsize, help="Max PRs to open in one run.")) -> None:
    """Deploy infrastructure changes by commenting 'atlantis apply' on PRs."""
    if state := state_object_handler.get_user_state():
        atlantis_apply(state, max_prs)
    else:
        sys.exit(1)
    print("\n[yellow] Hint: You can use 'dpteam pr probe apply' to see the status of Atlantis apply before attempting a merge.")
    print("[yellow]Next step: Perhaps you would want to run 'dpteam pr merge' when the applies are successful?")
