"""Auth related commands.

Commands invoked by dpteam auth <some-command> are defined here.
"""
from typing import Optional

import jwt
import pendulum
import typer
from rich.console import Console
from rich.style import Style

from dapla_team_cli.auth.services.get_token import get_token
from dapla_team_cli.auth.services.set_token import set_token


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}

app = typer.Typer(name="auth", help="Authenticate dpteam with Keycloak.", no_args_is_help=True)


@app.command()
def login(
    keycloak_token: Optional[str] = typer.Option(None, "-wt", "--with-token", help="Keycloak access token")  # noqa: B008
) -> None:
    """Authenticate with Keycloak.

    The default authentication mode is a web-based browser flow. After
    completion, an access token will be stored internally.

    Alternatively, use `--with-token` to pass in a token on standard input.

    You need to be logged in to communicate with backend APIs
    such as the dapla-team-api.
    """
    set_token(keycloak_token)


@app.command()
def status(raw_token: bool = typer.Option(False, "--raw-token", "-t", help="Print raw token")) -> None:  # noqa: B008
    """Show information about the current authentication status."""
    keycloak_token = get_token()

    if keycloak_token:
        dec_token = jwt.decode(keycloak_token, options={"verify_signature": False})
        expiry_date = pendulum.from_timestamp(dec_token["exp"], tz="local")
        console.print(f"Identity: {dec_token['name']} <{dec_token['email']}>", style=styles["normal"])
        console.print(f"Expiry date: {expiry_date.format('YYYY/MM/DD HH:mm:ss')}", style=styles["normal"])
        if expiry_date < pendulum.now("local"):
            console.print("Your token has expired. Please run dpteam auth login to fetch a new one.", style=styles["warning"])
        if raw_token:
            console.print(f"Raw token: {keycloak_token}", soft_wrap=True, style=styles["normal"])
    else:
        console.print(
            "You do not have a keycloak token set. Please run dpteam auth login --with-token <your_token> in order to add it.",
            style=styles["normal"],
        )
