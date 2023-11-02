"""Functionality related to asking the user for GCP project roles."""
from typing import List

import questionary as q

from dapla_team_cli import prompt_custom_style
from dapla_team_cli.gcp import GCPRole
from dapla_team_cli.gcp import GCPRoleValidator
from dapla_team_cli.gcp import gcp_project_roles


def ask_for_role() -> str:
    """Ask for one GCP role."""
    choices = [str(item["name"]) for item in gcp_project_roles.values()]
    meta_information = {
        item["name"]: f"{item['title']} - {item['description']}" if item.get("description") else item["title"]
        for item in gcp_project_roles.values()
    }
    return str(
        q.autocomplete(
            message="IAM Role",
            choices=choices,
            meta_information=meta_information,
            style=prompt_custom_style,
            validate=GCPRoleValidator,
        ).ask()
    )


def ask_for_project_roles(auth_group: str) -> List[GCPRole]:
    """Ask the user for GCP roles to which project-wide access should be granted.

    Args:
        auth_group: The auth group name, used for customizing the prompts

    Returns:
        A list of GCP roles
    """
    project_roles: List[GCPRole] = []

    if not q.confirm(f"Should {auth_group} be assigned any GCP IAM project roles?").ask():
        return project_roles

    q.print("(hit enter when done)")
    project_roles_set = set()
    role_name = ask_for_role()
    while role_name:
        project_roles_set.add(role_name)
        role_name = ask_for_role()

    project_roles = [GCPRole.parse_obj(gcp_project_roles[role]) for role in project_roles_set]

    return project_roles
