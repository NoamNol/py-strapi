import aiohttp
from typing import Any

from pystrapi._utils import run_async_safe
from pystrapi.errors import JsonParsingError
from pystrapi.help import helpers


async def load_response_json(response: aiohttp.ClientResponse, action: str) -> Any:
    try:
        return await response.json()
    except Exception as e:
        text = await run_async_safe(response.text, response.reason)
        raise JsonParsingError(f'Unable to {action}, status code: {response.status}, response: {text}') from e


async def raise_for_response(response: aiohttp.ClientResponse, action: str) -> None:
    """Raise suitable Strapi exception if response status code is above (or equal to) 400."""
    if response.status >= 400:
        data = await load_response_json(response, action)
        helpers.raise_for_strapi_response(data, response.status, action)
