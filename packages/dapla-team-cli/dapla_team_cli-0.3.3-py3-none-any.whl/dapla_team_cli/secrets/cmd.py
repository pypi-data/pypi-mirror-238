"""GCP Secrets related commands."""

import logging
import subprocess
import sys
from typing import Optional

import questionary as q
import typer
from google.api_core.exceptions import PermissionDenied
from google.auth.exceptions import DefaultCredentialsError
from rich.console import Console

from dapla_team_cli.secrets.services import SecretSession
from dapla_team_cli.secrets.services import get_secret_client


app = typer.Typer(no_args_is_help=True)

console = Console()

logger = logging.getLogger("dpteam")


@app.callback()
def secrets() -> None:
    """Manage a team's GCP secrets."""
    pass


@app.command()
def create(
    project_id: Optional[str] = typer.Option(None, "--payload", "-p", help="The secret data/payload"),  # noqa: B008
    secret_id: Optional[str] = typer.Option(None, "--secret-id", "-sid", help="ID of the secret, e.g. 'my-secret'"),  # noqa: B008
    payload: Optional[str] = typer.Option(  # noqa: B008
        None,
        "--project-id",
        "-pid",
        help="GCP project ID, e.g. 'dev-demo-example-1234'",
    ),
) -> None:
    """Create a new Secret Manager secret."""
    try:
        client = get_secret_client()

    except DefaultCredentialsError:
        print("You need to authenticate using `gcloud auth application-default login` before using `dpteam secrets`.")
        permission = q.confirm("Do you wish to do so now?").ask()
        if not permission:
            sys.exit(1)

        subprocess.run(["gcloud", "auth", "application-default", "login"], check=True)
        create(project_id, secret_id, payload)
        return

    actual_pid: str = (
        q.text("What is the ID of the GCP project the secret should reside in?").ask() if project_id is None else project_id
    )
    actual_sid: str = q.text("Secret ID?").ask() if secret_id is None else secret_id

    actual_payload: str = q.text("Secret Payload?").ask() if payload is None else payload

    session = SecretSession(actual_pid, actual_sid, actual_payload, client)

    try:
        session.request_creation()
    except PermissionDenied as e:
        logger.debug("permission error creating secret: %s", str(e))
        console.print(
            ("You are missing permissions to create secrets.\n"),
            ("Give your auth group permission through your team's IaC repo, for example using `dpteam tf iam-bindings`."),
        )
        sys.exit(1)

    try:
        session.add_version()
    except PermissionDenied as e:
        logger.debug("permission error adding secret version: %s", str(e))
        console.print(
            ("You are missing permissions to create secret versions/update secrets.\n"),
            ("Give your auth group permission through your team's IaC repo, for example using `dpteam tf iam-bindings`."),
        )
        sys.exit(1)

    print("The secret was successfully created")
