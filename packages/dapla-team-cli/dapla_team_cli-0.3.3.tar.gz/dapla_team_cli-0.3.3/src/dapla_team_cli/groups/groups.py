"""Add or remove teams with respective groups."""

from typing import List

from returns.pipeline import flow
from returns.pointfree import alt
from rich import print

from dapla_team_cli.api.api_request import DaplaTeamApiRequest
from dapla_team_cli.api.api_request import TeamGroupsBody
from dapla_team_cli.api.utils import delete_resource
from dapla_team_cli.api.utils import post_resource
from dapla_team_cli.config import DAPLA_TEAM_API_BASE
from dapla_team_cli.result_utils import fail


def add(team_name: str, group_suffixes: List[str]) -> None:
    """Adds a team with respective groups."""
    print("⚠️[yellow]  WARNING: This may take a few minutes")
    flow(
        DaplaTeamApiRequest(
            endpoint=f"{DAPLA_TEAM_API_BASE}/teams/{team_name}/groups", body=TeamGroupsBody(groupSuffixes=group_suffixes)
        ),
        post_resource,
        alt(fail),
    )


def remove(team_name: str, group_suffixes: List[str]) -> None:
    """Removes a team with respective groups."""
    flow(
        DaplaTeamApiRequest(
            endpoint=f"{DAPLA_TEAM_API_BASE}/teams/{team_name}/groups", body=TeamGroupsBody(groupSuffixes=group_suffixes)
        ),
        delete_resource,
        alt(fail),
    )
