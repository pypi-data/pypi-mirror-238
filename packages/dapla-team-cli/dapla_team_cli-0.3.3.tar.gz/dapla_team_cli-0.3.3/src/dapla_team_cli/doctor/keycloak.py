"""Checks for Keycloak token."""
import logging

import questionary as q
from jwt import DecodeError

from dapla_team_cli.auth.services.expiry import has_expired
from dapla_team_cli.auth.services.get_token import get_token
from dapla_team_cli.auth.services.set_token import set_token
from dapla_team_cli.doctor.check import Check
from dapla_team_cli.doctor.check import Failure
from dapla_team_cli.doctor.check import Success


logger = logging.getLogger("dpteam")


def get_new_token(state: str, re: bool = False) -> Check:
    """Ask if user wants to set a new token."""
    permission = q.confirm(f"Keycloak token {state}, do you want to {'re' if re else ''}authenticate?").ask()
    if not permission:
        return Failure(message=f"❌ Keycloak token {state}")

    set_token(None)
    return check_keycloak()


def check_keycloak() -> Check:
    """Check if the Keycloak token is set and valid."""
    token = get_token()

    if not token:
        return get_new_token("is not set")
    try:
        expired = has_expired(token)
        if expired:
            return get_new_token("has expired")

    except DecodeError:
        logger.debug("invalid token: %s", token)
        return get_new_token("is invalid", True)

    return Success(message="✅ Keycloak token is set and valid")
