"""Commands for starting or removing transfer service."""
from typing import Optional

import typer

from dapla_team_cli.team import get_team_name
from dapla_team_cli.transfer_service.transfer_service import add_ts
from dapla_team_cli.transfer_service.transfer_service import remove_ts


app = typer.Typer(name="ts", help="Create or remove a Transfer Service", no_args_is_help=True)


@app.command("add")
def add(
    team_name: Optional[str] = typer.Option(None, "--team-name", "-tn", help="Team name (e.g. demo-enhjoern-a)")  # noqa: B008
) -> None:
    """Add a transfer service for a team."""
    if team_name is None:
        team_name = get_team_name()
    add_ts(team_name)


@app.command("remove")
def remove(
    team_name: Optional[str] = typer.Option(None, "--team-name", "-tn", help="Team name (e.g. demo-enhjoern-a)")  # noqa: B008
) -> None:
    """Remove a transfer service for a team."""
    if team_name is None:
        team_name = get_team_name()
    remove_ts(team_name)
