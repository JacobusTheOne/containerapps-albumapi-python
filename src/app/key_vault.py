
import os
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


@lru_cache
def get_secret_client():
    """
    Create and cache a Key Vault client.

    Locally, DefaultAzureCredential can use Azure CLI authentication.
    In Azure Container Apps, it can use the attached managed identity.
    """

    vault_url = os.getenv("KEY_VAULT_URL")

    if not vault_url:
        raise RuntimeError("KEY_VAULT_URL environment variable is not set")

    credential = DefaultAzureCredential(
        managed_identity_client_id=os.getenv(
            "KEY_VAULT_MANAGED_IDENTITY_CLIENT_ID"
        )
    )

    return SecretClient(
        vault_url=vault_url,
        credential=credential
    )


def get_secret(secret_name: str) -> str:
    """
    Retrieve a secret value from Azure Key Vault.
    """

    client = get_secret_client()

    secret = client.get_secret(secret_name)

    return secret.value
