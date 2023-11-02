"""Commands editing members in groups."""
from typing import Optional

import typer

from dapla_team_cli.config import in_ipython_session
from dapla_team_cli.groups.members.members import add_members
from dapla_team_cli.groups.members.members import list_members
from dapla_team_cli.groups.members.members import remove_members
from dapla_team_cli.team import get_team_name
from dapla_team_cli.tf.iam_bindings.auth_groups import ask_for_auth_group_name
from dapla_team_cli.user import ask_for_users


app = typer.Typer(name="members", help="Commands for members", no_args_is_help=True)


def list(
    team_name: Optional[str] = typer.Option(None, "--team-name", "-tn", help="Team name (e.g. demo-enhjoern-a)")  # noqa: B008
) -> None:
    """List groups (and members) for a team."""
    if team_name is None:
        team_name = get_team_name()
    # team = get_remote_from_name(team_name)
    list_members(team_name)


def add(
    team_name: Optional[str] = typer.Option(None, "--team-name", "-tn", help="Team name (e.g. demo-enhjoern-a)"),  # noqa: B008
    members: Optional[str] = typer.Option(
        None, "--members", "-m", help="Space separated list of users (e.g. 'abc@ssb.no xyz@ssb.no'"
    ),  # noqa: B008
) -> None:
    """Adds members to a group."""
    if team_name is None:
        team_name = get_team_name()

    group_name = ask_for_auth_group_name(team_name)
    if members is None:
        members_list = ask_for_users()
    else:
        members_list = members.split(" ")
    # team_name = get_remote_from_name(team_name).name
    add_members(group_name, members_list)


def remove(
    team_name: Optional[str] = typer.Option(None, "--team-name", "-tn", help="Team name (e.g. demo-enhjoern-a)"),  # noqa: B008
    members: Optional[str] = typer.Option(
        None, "--members", "-m", help="Space separated list of users (e.g. 'abc@ssb.no xyz@ssb.no')"
    ),  # noqa: B008
) -> None:
    """Removes member from a group."""
    if team_name is None:
        team_name = get_team_name()

    group_name = ask_for_auth_group_name(team_name)
    if members is None:
        members_list = ask_for_users(group_name)
    else:
        members_list = members.split(" ")
    # team_name = get_remote_from_name(team_name).name
    remove_members(group_name, members_list)


app.command("list")(list)
if not in_ipython_session:
    app.command("add")(add)
    app.command("remove")(remove)
