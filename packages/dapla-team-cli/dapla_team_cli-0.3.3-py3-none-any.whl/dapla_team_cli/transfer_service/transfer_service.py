"""Adds or removes transfer service for a team."""

from returns.pipeline import flow
from returns.pointfree import alt

from dapla_team_cli.api.api_request import DaplaTeamApiRequest
from dapla_team_cli.api.utils import delete_resource
from dapla_team_cli.api.utils import post_resource
from dapla_team_cli.config import DAPLA_TEAM_API_BASE
from dapla_team_cli.result_utils import fail


def add_ts(team_name: str) -> None:
    """Adds a transfer service for a team."""
    flow(
        DaplaTeamApiRequest(endpoint=f"{DAPLA_TEAM_API_BASE}/teams/{team_name}/services/transfer-service", body=None),
        post_resource,
        alt(fail),
    )


def remove_ts(team_name: str) -> None:
    """Removes a transfer service for a team."""
    flow(
        DaplaTeamApiRequest(endpoint=f"{DAPLA_TEAM_API_BASE}/teams/{team_name}/services/transfer-service", body=None),
        delete_resource,
        alt(fail),
    )
