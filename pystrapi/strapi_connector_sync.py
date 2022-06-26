from abc import abstractmethod
from typing import Any, Dict, Protocol

import requests

from ._utils import getattrs_safe


class ConnectorSync(Protocol):
    api_url: str

    @abstractmethod
    def get(self, endpoint: str, *, reqargs: Dict[str, Any] = None, session: requests.Session = None) -> Any:
        """Send HTTP GET request and load response text as json"""

    @abstractmethod
    def post(self, endpoint: str, *, reqargs: Dict[str, Any] = None, session: requests.Session = None) -> Any:
        """Send HTTP POST request and load response text as json"""

    @abstractmethod
    def put(self, endpoint: str, *, reqargs: Dict[str, Any] = None, session: requests.Session = None) -> Any:
        """Send HTTP PUT request and load response text as json"""

    @abstractmethod
    def delete(self, endpoint: str, *, reqargs: Dict[str, Any] = None, session: requests.Session = None) -> Any:
        """Send HTTP DELETE request and load response text as json"""


class DefaultConnectorSync(ConnectorSync):
    """Default connector. Used if no custom connector was given"""

    def __init__(self, api_url: str):
        self.api_url = api_url

    def _request(
        self, method: str, endpoint: str, *, reqargs: Dict[str, Any] = None, session: requests.Session = None
    ) -> requests.Response:
        reqargs = reqargs or {}
        url = self.api_url + endpoint
        try:
            if session:
                response = session.request(method=method, url=url, **reqargs)
            else:
                response = requests.request(method=method, url=url, **reqargs)
        except Exception as e:
            raise Exception(f"Unable to {method}, error: {e})") from e
        if not response.ok:
            status_code, text = getattrs_safe(response, "status_code", "text")
            raise Exception(f"Unable to {method}, status code: {status_code}, text: {text}")
        return response

    def get(self, endpoint: str, *, reqargs: Dict[str, Any] = None, session: requests.Session = None) -> Any:
        return self._request("GET", endpoint, reqargs=reqargs).json()

    def post(self, endpoint: str, *, reqargs: Dict[str, Any] = None, session: requests.Session = None) -> Any:
        return self._request("POST", endpoint, reqargs=reqargs).json()

    def put(self, endpoint: str, *, reqargs: Dict[str, Any] = None, session: requests.Session = None) -> Any:
        return self._request("PUT", endpoint, reqargs=reqargs).json()

    def delete(self, endpoint: str, *, reqargs: Dict[str, Any] = None, session: requests.Session = None) -> Any:
        return self._request("DELETE", endpoint, reqargs=reqargs).json()
