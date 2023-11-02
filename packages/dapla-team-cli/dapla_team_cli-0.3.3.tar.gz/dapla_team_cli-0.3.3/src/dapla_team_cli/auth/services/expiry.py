"""Functions for verifying Keycloak tokens."""
import jwt
import pendulum


def has_expired(token: str) -> bool:
    """Check if a token has expired.

    Does not check whether a token is valid or not, so might throw an exception.
    """
    decoded = jwt.decode(token, options={"verify_signature": False})
    expiry_date = pendulum.from_timestamp(decoded["exp"])
    return expiry_date < pendulum.now()
