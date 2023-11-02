"""Commmon team info logic."""
import logging
import os
import sys
import time
from typing import List

import git
import questionary as q
from git.exc import GitError
from pydantic import BaseModel
from returns.pipeline import flow
from returns.pipeline import is_successful
from returns.pointfree import map_
from returns.result import Result

from dapla_team_cli import prompt_custom_style
from dapla_team_cli.api.api_request import DaplaTeamApiRequest
from dapla_team_cli.api.models.team import Team
from dapla_team_cli.api.models.team import parse_teams
from dapla_team_cli.api.utils import get_resource
from dapla_team_cli.config import DAPLA_TEAM_API_BASE
from dapla_team_cli.config import get_config_folder_path


logger = logging.getLogger("dpteam")


class TeamRepoInfo(BaseModel):
    """Holds information about a team's IaC repository."""

    name: str
    remote_url: str
    clone_folder: str


def get_team_name() -> str:
    """Get team name.

    Gets it from IaC repo info if CWD is one, asks the user for a name otherwise.
    """
    if not is_iac_repo(os.getcwd()):
        return ask_for_team_name()

    repo_path = os.getcwd()
    logger.debug("current CWD: %s", repo_path)

    glocal = git.cmd.Git(repo_path)
    iac_repo_remote_url = str(glocal.execute(["git", "remote", "get-url", "origin"]))
    logger.debug("remote url: %s", iac_repo_remote_url)

    team_name = iac_repo_remote_url.rsplit("/", maxsplit=1)[-1].split(".")[0].replace("-iac", "")
    return team_name


def get_remote_from_name(team_name: str) -> TeamRepoInfo:
    """Finds the team's name, remote IaC repo url and the local folder it should be cloned to."""
    iac_repo_remote_url = f"https://github.com/statisticsnorway/{team_name}-iac"
    iac_repo_clone_folder = f"{get_config_folder_path(tmp=True)}/{int(time.time())}-{team_name}"
    try:
        g = git.cmd.Git()
        g.execute(["git", "ls-remote", iac_repo_remote_url])
    except GitError as e:
        logger.debug("caught exception when getting remote: %s", str(e))
        if "not found" in str(e) or "error: 400" in str(e):
            print(f'Are you sure "{team_name}" is a valid team name? Its IaC repository could not be found.')
            sys.exit(1)
        else:
            print(f"Unknown error occured:\n{e}")
            sys.exit(1)

    return TeamRepoInfo(name=team_name, remote_url=iac_repo_remote_url, clone_folder=iac_repo_clone_folder)


def ask_for_team_name() -> str:
    """Ask for team name."""
    teams: Result[List[Team], str] = flow(
        DaplaTeamApiRequest(endpoint=f"{DAPLA_TEAM_API_BASE}/teams", body=None), get_resource, map_(parse_teams)
    )
    if not is_successful(teams):
        if "401" in teams.failure():
            print("Autocomplete unavailable due to authentication failure.")
            if os.getenv("NB_USER") != "jovyan":
                print("You may need to run `dpteam auth login` to fix it.")
        logger.debug("failure getting list of teams: %s", teams.failure())
        team_choices = [f"Autocomplete unavailable due to: {teams.failure()}"]
    else:
        team_choices = [team.uniform_team_name for team in teams.unwrap()]
    team_name = q.autocomplete(message="Team name (without the -iac suffix)", choices=team_choices, style=prompt_custom_style).ask()

    return str(team_name)


def is_iac_repo(path: str) -> bool:
    """Check if the given path is an IaC repo."""
    return os.path.isfile(path + "/terraform.tfvars")
