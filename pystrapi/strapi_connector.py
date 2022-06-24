from abc import abstractmethod
from typing import Any, Protocol
import aiohttp


class StrapiConnector(Protocol):
    api_url: str

    @abstractmethod
    async def get(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        """Send HTTP GET request and load response text as json"""

    @abstractmethod
    async def post(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        """Send HTTP POST request and load response text as json"""

    @abstractmethod
    async def put(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        """Send HTTP PUT request and load response text as json"""

    @abstractmethod
    async def delete(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        """Send HTTP DELETE request and load response text as json"""


class DefaultStrapiConnector(StrapiConnector):
    """Default strapi connector. Used if no custom connector was given"""

    def __init__(self, api_url: str):
        self.api_url = api_url

    async def _request(
        self, method: str, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None
    ) -> Any:
        async def only_ok_response(session: aiohttp.ClientSession, url: str, reqargs: dict) -> Any:
            try:
                async with session.request(method=method, url=url, **reqargs) as response:
                    if not response.ok:
                        try:
                            text: Any = await response.text()
                        except Exception:
                            text = response.reason
                        raise Exception(f"Unable to {method}, status code: {response.status}, text: {text}")
                    return await response.json()
            except Exception as e:
                raise Exception(f"Unable to {method}, error: {e})") from e
        reqargs = reqargs or {}
        url = self.api_url + endpoint
        if session:
            return await only_ok_response(session, url, reqargs)
        else:
            async with aiohttp.ClientSession() as session:
                return await only_ok_response(session, url, reqargs)

    async def get(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request("GET", endpoint, reqargs=reqargs)

    async def post(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request("POST", endpoint, reqargs=reqargs)

    async def put(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request("PUT", endpoint, reqargs=reqargs)

    async def delete(self, endpoint: str, *, reqargs: dict = None, session: aiohttp.ClientSession = None) -> Any:
        return await self._request("DELETE", endpoint, reqargs=reqargs)
