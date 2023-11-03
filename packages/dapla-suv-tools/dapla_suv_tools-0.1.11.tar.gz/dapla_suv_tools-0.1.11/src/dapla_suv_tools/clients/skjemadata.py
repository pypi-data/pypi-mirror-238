from datetime import date
import json
from typing import Optional

import dapla_suv_tools._internals.integration.api_client as api_client
from ssb_altinn3_util.models.skjemadata.skjemadata_request_models import SkjemaRequestModel


def get_skjema_by_id(skjema_id: int) -> dict:

    if not isinstance(skjema_id, int):
        raise ValueError("Field 'skjema_id' must be a valid integer")

    try:
        content: str = api_client._get(path=f"/skjemadata/skjema/{skjema_id}")
        return json.loads(content)
    except Exception as e:
        raise Exception(f"Failed to fetch for id {skjema_id}", e)


def get_skjema_by_ra_nummer(ra_nummer: str, max_results: int = 10, latest_only: bool = False) -> dict:
    try:
        filters = {"ra_nummer": ra_nummer}
        content: str = api_client._post(
            path=f"/skjemadata/skjema_paged?size={max_results}&order_by=versjon&asc=false", body=filters
        )

        result: dict = json.loads(content)

        if latest_only:
            return result["results"][0]

        return result["results"]

    except Exception as e:
        raise Exception(f"Failed to fetch for ra_nummer '{ra_nummer}'.", e)


def create_skjema(
        ra_nummer: str,
        versjon: int,
        undersokelse_nr: str,
        gyldig_fra: date,
        endret_av: str,
        datamodell: Optional[str] = None,
        beskrivelse: Optional[str] = None,
        navn_nb: Optional[str] = None,
        navn_nn: Optional[str] = None,
        navn_en: Optional[str] = None,
        infoside: Optional[str] = None,
        eier: Optional[str] = None,
        kun_sky: bool = False,
        gyldig_til: Optional[date] = None,
) -> int:
    model = SkjemaRequestModel(
        ra_nummer=ra_nummer,
        versjon=versjon,
        undersokelse_nr=undersokelse_nr,
        gyldig_fra=gyldig_fra,
        gyldig_til=gyldig_til,
        endret_av=endret_av,
        datamodell=datamodell,
        beskrivelse=beskrivelse,
        navn_nb=navn_nb,
        navn_nn=navn_nn,
        navn_en=navn_en,
        infoside=infoside,
        eier=eier,
        kun_sky="J" if kun_sky else "N"
    )

    try:
        body = model.model_dump()
        content: str = api_client._post(path=f"/skjemadata/skjema", body=body)
        return json.loads(content)[id]
    except Exception as e:
        raise Exception(f"Failed to create for ra_number '{ra_nummer}' - version '{versjon}'", e)


def delete_skjema(skjema_id: int) -> bool:
    pass


def get_periode_by_id(periode_id: int) -> dict:
    try:
        content: str = api_client._get(path=f"/skjemadata/periode/{periode_id}")
        return json.loads(content)
    except Exception as e:
        raise Exception(f"Failed to fetch for id {periode_id}", e)


def get_perioder_by_skjema_id(skjema_id: int) -> dict:
    try:
        content: str = api_client._get(path=f"/skjemadata/periode/skjema/{skjema_id}")
        return json.loads(content)
    except Exception as e:
        raise Exception(f"Failed to fetch for id {skjema_id}", e)
