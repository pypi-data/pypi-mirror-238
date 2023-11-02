"""Provides functions used to manage secrets."""
import os

import requests
from google.cloud import secretmanager
from google.cloud.secretmanager import SecretManagerServiceClient
from google.oauth2.credentials import Credentials
from jupyterhub.services.auth import HubAuth


class SecretSession:
    """Holds information about the current secret creation session."""

    def __init__(self, project_id: str, secret_id: str, payload: str, client: SecretManagerServiceClient) -> None:
        """Initialize secret info and encode payload."""
        self.project_id = project_id
        self.secret_id = secret_id
        self.payload = payload.encode("UTF-8")
        self.client = client

    def request_creation(self) -> None:
        """Requests google cloud storage client to create a secret."""
        parent = f"projects/{self.project_id}"

        response = self.client.create_secret(
            request={
                "parent": parent,
                "secret_id": self.secret_id,
                "secret": {"replication": {"user_managed": {"replicas": [{"location": "europe-north1"}]}}},
            }
        )

        print(f"Created secret: {response.name}")

    def add_version(self) -> None:
        """Requests google cloud storage client to create a secret."""
        parent = self.client.secret_path(self.project_id, self.secret_id)

        response = self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": self.payload},
            }
        )

        print(f"Added secret version: {response.name}")


def get_secret_client() -> SecretManagerServiceClient:
    """Get a secret manager seervice client instance.

    If in a jupyterhub environment, use HubAuth, otherwise use application default credentials.
    """
    if os.getenv("NB_USER") != "jovyan":
        return secretmanager.SecretManagerServiceClient()

    hub = HubAuth()
    response = requests.get(
        os.environ["LOCAL_USER_PATH"],
        headers={"Authorization": "token {hub.api_token}"},
        cert=(str(hub.certfile), str(hub.keyfile)),
        verify=str(hub.client_ca),
        allow_redirects=False,
        timeout=10,
    )

    token = response.json()["exchanged_tokens"]["google"]["access_token"]
    credentials = Credentials(token=token)
    return secretmanager.SecretManagerServiceClient(credentials=credentials)
