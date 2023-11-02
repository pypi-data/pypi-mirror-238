"""Commmon user info logic."""
import logging
import os
from typing import List
from typing import Optional

import questionary as q
from questionary import confirm
from returns.pipeline import flow
from returns.pipeline import is_successful
from returns.pointfree import map_
from returns.result import Result

from dapla_team_cli import prompt_custom_style
from dapla_team_cli.api.api_request import DaplaTeamApiRequest
from dapla_team_cli.api.models.user import User
from dapla_team_cli.api.models.user import parse_users
from dapla_team_cli.api.utils import get_resource
from dapla_team_cli.config import DAPLA_TEAM_API_BASE


logger = logging.getLogger("dpteam")


def ask_for_users(group_name: Optional[str] = None) -> List[str]:
    """Ask for user name."""
    if group_name is None:
        endpoint = DAPLA_TEAM_API_BASE
    else:
        endpoint = f"{DAPLA_TEAM_API_BASE}/groups/{group_name}"
    users: Result[List[User], str] = flow(
        DaplaTeamApiRequest(endpoint=f"{endpoint}/users", body=None), get_resource, map_(parse_users)
    )
    if not is_successful(users):
        if "401 Unauthorized" in users.failure():
            print("Autocomplete unavailable due to authentication failure.")
            if os.getenv("NB_USER") != "jovyan":
                print("You may need to run `dpteam auth login` to fix it.")
        logger.debug("failure getting list of teams: %s", users.failure())
        user_choices = [f"Autocomplete unavailable due to: {users.failure()}"]
    else:
        user_choices = [user.email_short for user in users.unwrap()]

    chosen_users: List[str] = []
    while True:
        user = q.autocomplete(
            message="Short-form username (e.g. abc@ssb.no) (Enter to skip)", choices=user_choices, style=prompt_custom_style
        ).ask()
        if user != "":
            chosen_users.append(user)

        if not confirm("Do you want to keep adding users?").ask():
            break

    return chosen_users
