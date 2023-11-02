"""Model for a dapla-team-api link resource."""
from pydantic import BaseModel


class Link(BaseModel):
    """A Link resource in the API."""

    href: str
