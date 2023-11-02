"""Utility functions for interacting with dapla-team-api."""
import json
import logging
from typing import Any
from typing import Dict

import requests
from returns.result import Failure
from returns.result import Result
from returns.result import Success

from dapla_team_cli.api.api_request import DaplaTeamApiRequest
from dapla_team_cli.auth.services.get_token import get_token


logger = logging.getLogger("dpteam")


def get_resource(request: DaplaTeamApiRequest) -> Result[Dict[str, Any], str]:
    """Get a given resource (Team/Group/User/a list) from the API."""
    token = get_token()
    logger.debug(f"Endpoint is {request.endpoint}")
    try:
        response = requests.get(
            request.endpoint,
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )
    except requests.RequestException as e:
        logger.debug("exception thrown in get_resource accessing %s, exception: %s", request.endpoint, str(e))
        return Failure("Something went wrong trying to access the API")

    if response.status_code != 200:
        logger.debug(
            "get_resource got status code %s accessing %s | Reason: %s | Response body: %s",
            response.status_code,
            request.endpoint,
            response.reason,
            response.content.decode("utf-8"),
        )
        return Failure(f"Error trying to access {request.endpoint}: {response.status_code} {response.reason}")

    return Success(response.json())


def post_resource(request: DaplaTeamApiRequest) -> Result[Dict[str, Any], str]:
    """Get a given resource (Team/Group/User/a list) from the API."""
    logger.debug(f"Endpoint is {request.endpoint}")
    if request.body is not None:
        json_body = request.body.json()
        logger.debug(f"Body is {json_body}")
    else:
        json_body = None

    token = get_token()
    try:
        response = requests.post(
            url=request.endpoint,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            data=json_body,
            timeout=300,
        )
    except requests.RequestException as e:
        logger.debug("exception thrown in get_resource accessing %s, exception: %s", request.endpoint, str(e))
        return Failure("Something went wrong trying to access the API")

    pretty_reponse = json.dumps(response.json(), indent=4)
    logger.debug(f"Response: \n {pretty_reponse}")

    if response.status_code not in (200, 201):
        logger.debug(
            "post_resource got status code %s accessing %s | Reason: %s | Response body: %s",
            response.status_code,
            request.endpoint,
            response.reason,
            response.content.decode("utf-8"),
        )
        return Failure(f"Error trying to access {request.endpoint}: {response.status_code} {response.reason}")

    return Success(response.json())


def delete_resource(request: DaplaTeamApiRequest) -> Result[Dict[str, Any], str]:
    """Get a given resource (Team/Group/User/a list) from the API."""
    token = get_token()
    logger.debug(f"Endpoint is {request.endpoint}")
    if request.body is not None:
        json_body = request.body.json()
        logger.debug(f"Body is {request.body.json()}")
    else:
        json_body = None

    try:
        response = requests.delete(
            url=request.endpoint,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            data=json_body,
            timeout=300,
        )
    except requests.RequestException as e:
        logger.debug("exception thrown in get_resource accessing %s, exception: %s", request.endpoint, str(e))
        return Failure("Something went wrong trying to access the API")

    pretty_reponse = json.dumps(response.json(), indent=4)
    logger.debug(f"Response: \n {pretty_reponse}")

    if response.status_code not in (200, 201):
        logger.debug(
            "delete_resource got status code %s accessing %s | Reason: %s | Response body: %s",
            response.status_code,
            request.endpoint,
            response.reason,
            response.content.decode("utf-8"),
        )
        return Failure(f"Error trying to access {request.endpoint}: {response.status_code} {response.reason}")

    return Success(response.json())
