"""API Request BaseModel."""
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel


class TeamGroupsBody(BaseModel):
    """Request Body when operating on Team groups."""

    groupSuffixes: List[str]  # noqa: N815


class UserBody(BaseModel):
    """Request body when operating on User bodies."""

    users: List[str]


class DaplaTeamApiRequest(BaseModel):
    """Request model for interacting with Dapla Team API."""

    endpoint: str
    body: Optional[Union[TeamGroupsBody, UserBody]]
