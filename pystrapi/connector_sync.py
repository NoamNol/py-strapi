from abc import abstractmethod
from typing import Any, Protocol
import requests

from .errors import JsonParsingError, StrapiError
from .helpers import raise_for_response
from ._utils import getattr_safe


class ConnectorSync(Protocol):
    @abstractmethod
    def request(
        self, method: str, url: str, *, reqargs: dict = None, session: requests.Session = None
    ) -> requests.Response:
        """Send HTTP request and load response."""


class DefaultConnectorSync(ConnectorSync):
    """Default connector. Used if no custom connector was given."""

    def request(
        self, method: str, url: str, *, reqargs: dict = None, session: requests.Session = None
    ) -> requests.Response:
        reqargs = reqargs or {}
        try:
            if session:
                response = session.request(method=method, url=url, **reqargs)
            else:
                response = requests.request(method=method, url=url, **reqargs)
        except Exception as e:
            raise StrapiError(f"Unable to {method}, error: {e})") from e
        return response


class ConnectorWrapperSync:
    """Wrapper around the connector.
    - Send requests using the connector.
    - Parse response as json.
    - Raise custom strapi exceptions for different types of bad response.
    """

    def __init__(self, api_url: str, connector: ConnectorSync):
        self.api_url = api_url
        self._connector = connector

    def _request(
        self, method: str, endpoint: str, *, reqargs: dict = None, session: requests.Session = None
    ) -> Any:
        url = self.api_url + endpoint
        action = f'send {method} to {url}'
        response = self._connector.request(method, url, reqargs=reqargs, session=session)
        status_code = response.status_code
        try:
            data = response.json()
        except Exception as e:
            text = getattr_safe(response, "text", response.reason)
            raise JsonParsingError(f"Unable to {action}, status code: {status_code}, response: {text}") from e
        raise_for_response(data, status_code, action)
        return data

    def get(self, endpoint: str, *, reqargs: dict = None, session: requests.Session = None) -> Any:
        return self._request("GET", endpoint, reqargs=reqargs, session=session)

    def post(self, endpoint: str, *, reqargs: dict = None, session: requests.Session = None) -> Any:
        return self._request("POST", endpoint, reqargs=reqargs, session=session)

    def put(self, endpoint: str, *, reqargs: dict = None, session: requests.Session = None) -> Any:
        return self._request("PUT", endpoint, reqargs=reqargs, session=session)

    def delete(self, endpoint: str, *, reqargs: dict = None, session: requests.Session = None) -> Any:
        return self._request("DELETE", endpoint, reqargs=reqargs, session=session)
