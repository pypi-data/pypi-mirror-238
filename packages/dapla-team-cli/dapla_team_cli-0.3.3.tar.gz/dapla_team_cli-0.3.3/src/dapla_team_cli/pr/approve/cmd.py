"""Commands for approving pull requests."""

import sys

from dapla_team_cli.pr.approve.approve import approve_prs
from dapla_team_cli.pr.state.state_utils import state_object_handler


def approve() -> None:
    """Approves all pull requests."""
    if state := state_object_handler.get_user_state():
        approve_prs(state)
    else:
        sys.exit(1)
