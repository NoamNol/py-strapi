from typing import Any
import requests

from pystrapi.help import helpers

from pystrapi._utils import getattr_safe
from pystrapi.errors import JsonParsingError


def load_response_json(response: requests.Response, action: str) -> Any:
    try:
        return response.json()
    except Exception as e:
        text = getattr_safe(response, 'text', response.reason)
        raise JsonParsingError(f'Unable to {action}, status code: {response.status_code}, response: {text}') from e


def raise_for_response(response: requests.Response, action: str) -> None:
    """Raise suitable Strapi exception if response status code is above (or equal to) 400."""
    if response.status_code >= 400:
        data = load_response_json(response, action)
        helpers.raise_for_strapi_response(data, response.status_code, action)
