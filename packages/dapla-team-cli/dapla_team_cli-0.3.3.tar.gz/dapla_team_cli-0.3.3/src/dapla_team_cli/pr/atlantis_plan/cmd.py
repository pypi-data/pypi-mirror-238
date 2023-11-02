"""Commands for writing 'atlantis plan' on PRs."""
import sys

import typer

from dapla_team_cli.pr.atlantis_plan.atlantis_plan_all import atlantis_plan
from dapla_team_cli.pr.state.state_utils import state_object_handler


def plan(max_prs: int = typer.Argument(sys.maxsize, help="Max PRs to open in one run.")) -> None:
    """Writes 'atlantis plan' on all PRs."""
    if state := state_object_handler.get_user_state():
        atlantis_plan(state, max_prs)
    else:
        sys.exit(1)
