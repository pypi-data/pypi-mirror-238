"""Groups related commands.

Commands invoked by dpteam groups <some-command> are defined here.
"""

from typing import List
from typing import Optional

import typer

import dapla_team_cli.groups.members.cmd as members
from dapla_team_cli.config import in_ipython_session
from dapla_team_cli.groups.groups import add
from dapla_team_cli.groups.groups import remove
from dapla_team_cli.pr.prompt_utils import confirm_input
from dapla_team_cli.team import get_team_name


app = typer.Typer(no_args_is_help=True)


@app.callback()
def groups() -> None:
    """Interact with a team's auth group memberships."""
    pass


def add_groups(
    team_name: Optional[str] = typer.Option(
        None, "--team-name", "-tn", help="Team names separated by space (e.g. 'dev-stat-a demo-stat-b')"
    )
) -> None:
    """Adds a team with respective groups."""
    if team_name is None:
        team_name = confirm_input("Provide the name of the team to be created")

    # team_name = get_remote_from_name(team_name).name
    group_suffixes: List[str] = []  # TODO: Add as CLI option
    add(team_name, group_suffixes)


def remove_groups(
    team_name: Optional[str] = typer.Option(None, "--team-name", "-tn", help="Team name (e.g. demo-enhjoern-a)")
) -> None:
    """Removes a team with respective groups."""
    if team_name is None:
        team_name = get_team_name()
    # team_name = get_remote_from_name(team_name).name
    group_suffixes: List[str] = []  # TODO: Add as CLI option
    remove(team_name, group_suffixes)


app.add_typer(members.app)
if not in_ipython_session:
    app.command("create")(add_groups)
    app.command("delete")(remove_groups)
