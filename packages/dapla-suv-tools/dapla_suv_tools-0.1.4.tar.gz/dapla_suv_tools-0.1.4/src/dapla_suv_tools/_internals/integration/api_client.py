import os
import requests

from dapla.auth import AuthClient

END_USER_API_BASE_URL = os.getenv("SUV_END_USER_API_URL")


def _get(path: str) -> str:

    headers = _get_headers()

    response = requests.get(f"{END_USER_API_BASE_URL}{path}", headers=headers)

    if not _success(response.status_code):
        error = response.content.decode("UTF-8")
        print(f"Error (status: {response.status_code}):  {error}")
        raise Exception("Failed to fetch.")

    return response.content.decode("UTF-8")


def _get_headers() -> dict:
    token: str = AuthClient.fetch_personal_token()

    return {
        "authorization": f"Bearer {token}"
    }


def _success(status_code: int) -> bool:
    return str(status_code).startswith("2")
