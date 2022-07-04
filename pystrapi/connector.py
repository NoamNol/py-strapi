from abc import abstractmethod
from typing import Any, Protocol
import aiohttp

from .errors import JsonParsingError, StrapiError
from .helpers import raise_for_response
from ._utils import run_async_safe


class Connector(Protocol):
    @abstractmethod
    async def request(
        self, method: str, url: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None
    ) -> aiohttp.ClientResponse:
        """Send HTTP request and load response. Can do things like custom exceptions, logs and cache."""


async def _load_response_json(response: aiohttp.ClientResponse, action: str) -> Any:
    try:
        return await response.json()
    except Exception as e:
        text = await run_async_safe(response.text, response.reason)
        raise JsonParsingError(f'Unable to {action}, status code: {response.status}, response: {text}') from e


class DefaultConnector(Connector):
    """Default connector. Used if no custom connector was given."""

    async def request(
        self, method: str, url: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None
    ) -> aiohttp.ClientResponse:
        reqargs = reqargs or {}
        if session:
            return await self._request_from_session(session, method, url, reqargs)
        else:
            async with aiohttp.ClientSession() as session:
                return await self._request_from_session(session, method, url, reqargs)

    async def _request_from_session(
        self, session: aiohttp.ClientSession, method: str, url: str, reqargs: dict
    ) -> aiohttp.ClientResponse:
        action = f'send {method} to {url}'
        try:
            response = await session.request(method=method, url=url, **reqargs)
        except Exception as e:
            raise StrapiError(f'Unable to {action}, error: {e})') from e
        data = await _load_response_json(response, action)
        raise_for_response(data, response.status, action)
        return response


class ConnectorWrapper:
    """Wrapper around the connector.
    - Send requests using the connector.
    - Parse response as json.

    Exceptions:
    - Exceptions from the connector
    - JsonParsingError
    - Strapi exceptions from `raise_for_response`
    """

    def __init__(self, api_url: str, connector: Connector):
        self.api_url = api_url
        self._connector = connector

    async def _request(
        self, method: str, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None
    ) -> Any:
        url = self.api_url + endpoint
        action = f'send {method} to {url}'
        response = await self._connector.request(method, url, reqargs=reqargs, session=session)
        data = await _load_response_json(response, action)
        response.release()
        raise_for_response(data, response.status, action)
        return data

    async def get(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request('GET', endpoint, reqargs=reqargs, session=session)

    async def post(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request('POST', endpoint, reqargs=reqargs, session=session)

    async def put(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request('PUT', endpoint, reqargs=reqargs, session=session)

    async def delete(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request('DELETE', endpoint, reqargs=reqargs, session=session)
