"""dapla-team-api User model."""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import parse_obj_as

from dapla_team_cli.api.models.link import Link


class User(BaseModel):
    """Information about a Dapla team member.

    Attributes:
        name: Display name from ad, such as `Nordmann, Ola`
        email: Email, such as `noo@ssb.no`
    """

    name: str
    email_short: str = Field(alias="emailShort")
    email: Optional[str]
    links: Dict[str, Link] = Field(alias="_links")


def parse_users(users: Dict[str, Any]) -> List[User]:
    """Parse JSON into a list of Members."""
    if "_embedded" not in users or "userList" not in users["_embedded"]:
        return []
    return parse_obj_as(List[User], users["_embedded"]["userList"])
