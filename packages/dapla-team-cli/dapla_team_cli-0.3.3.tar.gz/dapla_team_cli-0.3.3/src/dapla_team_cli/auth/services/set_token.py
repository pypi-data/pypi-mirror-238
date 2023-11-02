"""Set token helper function. Sets or updates Keycloak token on local machine."""
import json
import os
from typing import Union

import questionary as q
from rich.console import Console
from rich.style import Style

from dapla_team_cli.config import get_config_folder_path


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "error": Style(color="red", blink=True, bold=True),
    "success": Style(color="green", blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


def set_token(keycloak_token: Union[str, None]) -> None:
    """Sets or updates a keycloak token on users local machine."""
    config_folder_path = get_config_folder_path()

    if not keycloak_token:
        keycloak_token = q.text(
            "Please provide a Keycloak token. Please go to https://httpbin-fe.staging-bip-app.ssb.no/anything/bearer to fetch it:"
        ).ask()

    config_file_path = config_folder_path + "/dapla-cli-keycloak-token.json"

    if not os.path.exists(config_folder_path):
        os.makedirs(config_folder_path)

    data = {"keycloak_token": keycloak_token}

    with open(config_file_path, "w", encoding="UTF-8") as f:
        json.dump(data, f)

    console.print("Token was succesfully added.", style=styles["success"])
