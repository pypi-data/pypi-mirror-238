"""dapla-team-api Group model."""
from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field
from pydantic import parse_obj_as
from returns.result import Result

from dapla_team_cli.api.api_request import DaplaTeamApiRequest
from dapla_team_cli.api.models.link import Link
from dapla_team_cli.api.models.user import User
from dapla_team_cli.api.models.user import parse_users
from dapla_team_cli.api.utils import get_resource


class Group(BaseModel):
    """Information about a Dapla team auth group."""

    ID: str = Field(alias="id")
    azure_id: str = Field(alias="azureId")
    name: str
    links: Dict[str, Link] = Field(alias="_links")

    def users(self) -> Result[List[User], str]:
        """Get a list of Users in this group."""
        return get_resource(DaplaTeamApiRequest(endpoint=self.links["users"].href, body=None)).map(parse_users)


def parse_groups(groups_json: Dict[str, Any]) -> List[Group]:
    """Parse JSON into a list of Groups."""
    if "_embedded" not in groups_json or "groupList" not in groups_json["_embedded"]:
        return []
    return parse_obj_as(List[Group], groups_json["_embedded"]["groupList"])
