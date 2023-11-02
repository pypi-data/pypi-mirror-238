import json
from typing import Union

import dapla_suv_tools._internals.integration.api_client as api_client


def get_skjema_by_id(skjema_id: int) -> dict:

    if not isinstance(skjema_id, int):
        raise ValueError("Field 'skjema_id' must be a valid integer")

    try:
        content: str = api_client._get(path=f"/skjemadata/skjema/{skjema_id}")
        return json.loads(content)
    except Exception as e:
        raise Exception(f"Failed to fetch for id {skjema_id}", e)


def get_skjema_by_ra_nummer(ra_nummer: str, latest_only: bool = False) -> dict:
    try:
        filters = {"ra_nummer": ra_nummer}
        content: str = api_client._post(path=f"/skjemadata/skjema_paged?order_by=versjon&asc=false", data=filters)

        result: dict = json.loads(content)

        if latest_only:
            return result["results"][0]

        return result["results"]

    except Exception as e:
        raise Exception(f"Failed to fetch for ra_nummer '{ra_nummer}'.", e)


def create_skjema() -> int:
    pass


def delete_skjema(skjema_id: int) -> bool:
    pass


def get_periode_by_id(periode_id: int) -> dict:
    pass


def get_perioder_by_skjema_id(skjema_id: int) -> dict:
    pass
