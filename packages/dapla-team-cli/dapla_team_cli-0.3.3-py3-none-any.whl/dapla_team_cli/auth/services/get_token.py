"""Get token helper function. Retrieve the Keycloak token on local machine."""
import json
import logging
import os
from typing import Optional

import requests
import typer
from jupyterhub.services.auth import HubAuth
from rich.console import Console
from rich.style import Style

from dapla_team_cli.config import get_config_folder_path


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}

logger = logging.getLogger("dpteam")


def get_token() -> Optional[str]:
    """Retrieves token if it exists or returns None if no token exists.

    Returns:
        Either the Keycloak token, if it exists, or None if it does not exist.
    """
    # Taken from dapla-toolbelt
    if os.getenv("NB_USER") == "jovyan":
        hub = HubAuth()
        response = requests.get(
            os.environ["LOCAL_USER_PATH"],
            headers={"Authorization": f"token {hub.api_token}"},
            cert=(str(hub.certfile), str(hub.keyfile)),
            verify=str(hub.client_ca),
            allow_redirects=False,
            timeout=10,
        )
        if response.status_code != 200:
            logger.debug(
                "status code %d fetching token | reason: %s | response body: %s",
                response.status_code,
                response.reason,
                response.content.decode("utf-8"),
            )
            print("Error fetching token.")
            typer.Abort()
        token = str(response.json()["access_token"])
        if not token:
            logger.debug(
                "successful response fetching token, but token missing | response body: %s", response.content.decode("utf-8")
            )
            print("Token missing from auth response.")
            typer.Abort()
        return token

    config_folder_path = get_config_folder_path()
    config_file_path = config_folder_path + "/dapla-cli-keycloak-token.json"

    keycloak_token = None
    if os.path.isfile(config_file_path):
        with open(config_file_path, encoding="UTF-8") as f:
            data = json.loads(f.read())
            keycloak_token = data["keycloak_token"]

    if keycloak_token is None:
        logger.debug("keycloak token not set")

    return keycloak_token
