"""GCP specific stuff."""
import importlib.resources
import json

import questionary as q
from prompt_toolkit.document import Document
from pydantic import BaseModel


with importlib.resources.open_text("dapla_team_cli.gcp", "project_roles.json") as file:
    items = json.load(file)
    gcp_project_roles = {item["name"]: item for item in items}


class GCPRole(BaseModel):
    """A `GCPRole` holds information about a GCP role, such as name and description.

    Attributes:
        name: The technical name of the GCP role, such as `roles/bigquery.admin`
        title: A display friendly name, such as `BigQuery Admin`
        description: A descriptive text that gives a short presentation of the role,
            such as ``Administer all BigQuery resources and data
    """

    name: str
    title: str
    description: str

    def __eq__(self, __o: object) -> bool:
        """Custom equals operator, match on name."""
        if not isinstance(__o, GCPRole):
            return super().__eq__(__o)
        return self.name == __o.name

    def __lt__(self, __o: object) -> bool:
        """Implemented to support sorting."""
        if not isinstance(__o, GCPRole):
            raise NotImplementedError
        return self.name < __o.name

    def __hash__(self) -> int:
        """Implemented to support using GCPRole as a key in a dictionary."""
        return hash(self.name)


class GCPRoleValidator(q.Validator):
    """Questionary Validator used for checking if the user provided GCP role is properly formatted."""

    def validate(self, document: Document) -> None:
        """Validate that a GCP role name is appropriately formatted.

        Args:
            document: The document to validate

        Raises:
             ValidationError: if input does not adhere to the naming convention.
        """
        ok = not document.text or "roles/" in document.text and document.text in gcp_project_roles.keys()
        if not ok:
            raise q.ValidationError(message="Please choose a GCP Role", cursor_position=len(document.text))
