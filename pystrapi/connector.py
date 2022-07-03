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
        """Send HTTP request and load response."""


class DefaultConnector(Connector):
    """Default connector. Used if no custom connector was given."""

    async def request(
        self, method: str, url: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None
    ) -> aiohttp.ClientResponse:
        async def _request(session: aiohttp.ClientSession, url: str, reqargs: dict) -> aiohttp.ClientResponse:
            try:
                return await session.request(method=method, url=url, **reqargs)
            except Exception as e:
                raise StrapiError(f"Unable to {method}, error: {e})") from e
        reqargs = reqargs or {}
        if session:
            return await _request(session, url, reqargs)
        else:
            async with aiohttp.ClientSession() as session:
                return await _request(session, url, reqargs)


class ConnectorWrapper:
    """Wrapper around the connector.
    - Send requests using the connector.
    - Parse response as json.
    - Raise custom strapi exceptions for different types of bad response.
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
        status_code = response.status
        try:
            data = await response.json()
        except Exception as e:
            text = await run_async_safe(response.text, response.reason)
            raise JsonParsingError(f"Unable to {action}, status code: {status_code}, response: {text}") from e
        response.release()
        raise_for_response(data, status_code, action)
        return data

    async def get(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request("GET", endpoint, reqargs=reqargs, session=session)

    async def post(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request("POST", endpoint, reqargs=reqargs, session=session)

    async def put(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request("PUT", endpoint, reqargs=reqargs, session=session)

    async def delete(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request("DELETE", endpoint, reqargs=reqargs, session=session)
