import json
from typing import Union

import dapla_suv_tools._internals.integration.api_client as api_client


def get_skjema_by_id(skjema_id: int) -> Union[dict, str]:

    if not isinstance(skjema_id, int):
        return "Field 'skjema_id' must be a valid integer"

    try:
        content: str = api_client._get(path=f"/skjemadata/skjema/{skjema_id}")
        return json.loads(content)
    except Exception as e:
        return f"Failed to fetch for id"
