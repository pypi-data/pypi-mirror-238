"""dapla-team-api Team model."""
from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field
from pydantic import parse_obj_as
from returns.result import Result

from dapla_team_cli.api.api_request import DaplaTeamApiRequest
from dapla_team_cli.api.models.group import Group
from dapla_team_cli.api.models.group import parse_groups
from dapla_team_cli.api.models.link import Link
from dapla_team_cli.api.models.user import User
from dapla_team_cli.api.models.user import parse_users
from dapla_team_cli.api.utils import get_resource


class Team(BaseModel):
    """Information about a Dapla team."""

    uniform_team_name: str = Field(alias="uniformTeamName")
    display_team_name: str = Field(alias="displayTeamName")
    repo: str
    links: Dict[str, Link] = Field(alias="_links")

    def users(self) -> Result[List[User], str]:
        """Get a list of users in this team."""
        return get_resource(DaplaTeamApiRequest(endpoint=self.links["users"].href, body=None)).map(parse_users)

    def groups(self) -> Result[List[Group], str]:
        """Get a list of auth groups in this team."""
        return get_resource(DaplaTeamApiRequest(endpoint=self.links["groups"].href, body=None)).map(parse_groups)


def parse_teams(teams_json: Dict[str, Any]) -> List[Team]:
    """Parse JSON into a list of Teams."""
    if "_embedded" not in teams_json or "teamList" not in teams_json["_embedded"]:
        return []
    return parse_obj_as(List[Team], teams_json["_embedded"]["teamList"])
