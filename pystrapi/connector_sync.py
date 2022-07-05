from abc import abstractmethod
from typing import Any, Protocol
import requests

from .errors import StrapiError
from .help import requests_helpers
from .help.helpers import raise_for_strapi_response


class ConnectorSync(Protocol):
    @abstractmethod
    def request(
        self, method: str, url: str, *, reqargs: dict = None, session: requests.Session = None
    ) -> requests.Response:
        """Send HTTP request and load response. Can do things like custom exceptions, logs and cache."""


class DefaultConnectorSync(ConnectorSync):
    """Default connector. Used if no custom connector was given."""

    def request(
        self, method: str, url: str, *, reqargs: dict = None, session: requests.Session = None
    ) -> requests.Response:
        reqargs = reqargs or {}
        action = f'send {method} to {url}'
        try:
            if session:
                response = session.request(method=method, url=url, **reqargs)
            else:
                response = requests.request(method=method, url=url, **reqargs)
        except Exception as e:
            raise StrapiError(f'Unable to {action}, error: {e})') from e
        requests_helpers.raise_for_response(response, action)
        return response


class ConnectorWrapperSync:
    """Wrapper around the connector.
    - Send requests using the connector.
    - Parse response as json.

    Exceptions:
    - Exceptions from the connector
    - JsonParsingError
    - Strapi exceptions from `raise_for_response`
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
        data = requests_helpers.load_response_json(response, action)
        raise_for_strapi_response(data, response.status_code, action)
        return data

    def get(self, endpoint: str, *, reqargs: dict = None, session: requests.Session = None) -> Any:
        return self._request('GET', endpoint, reqargs=reqargs, session=session)

    def post(self, endpoint: str, *, reqargs: dict = None, session: requests.Session = None) -> Any:
        return self._request('POST', endpoint, reqargs=reqargs, session=session)

    def put(self, endpoint: str, *, reqargs: dict = None, session: requests.Session = None) -> Any:
        return self._request('PUT', endpoint, reqargs=reqargs, session=session)

    def delete(self, endpoint: str, *, reqargs: dict = None, session: requests.Session = None) -> Any:
        return self._request('DELETE', endpoint, reqargs=reqargs, session=session)
