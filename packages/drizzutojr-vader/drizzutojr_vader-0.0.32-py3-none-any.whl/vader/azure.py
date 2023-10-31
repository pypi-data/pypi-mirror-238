import os
import json

from .consts import DEFAULT_AZURE_CREDS_FILE

from msal import ConfidentialClientApplication

AZURE_CREDS_FILE = os.environ.get("AZURE_CREDS_FILE", DEFAULT_AZURE_CREDS_FILE)


def get_creds() -> dict:
    azure_creds = None
    with open(AZURE_CREDS_FILE, "r") as f:
        azure_creds = json.load(f)

    return azure_creds


def get_token():
    azure_creds = get_creds()

    app = ConfidentialClientApplication(
        client_id=azure_creds["client_id"],
        client_credential=azure_creds["client_secret"],
        authority=azure_creds["authority"],
    )

    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_for_client(scopes=scopes)

    return result.get("access_token")
