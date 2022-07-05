import requests
from typing import List, Optional, Union

from .errors import StrapiError
from .help.helpers import _stringify_parameters
from .parameters import PublicationState
from .connector_sync import ConnectorWrapperSync, DefaultConnectorSync, ConnectorSync
from .types import (
    PaginationParameter,
    PopulationParameter,
    StrapiAuthResponse,
    StrapiEntriesResponse,
    StrapiEntryResponse,
)


class StrapiClientSync:
    """REST API client for Strapi.

    Strapi docs:
    https://docs.strapi.io/developer-docs/latest/developer-resources/database-apis-reference/rest-api.html
    """

    def __init__(
        self, *,
        api_url: Optional[str] = None,
        connector: Optional[ConnectorSync] = None,
        token: Optional[str] = None,
    ):
        api_url = api_url or 'http://localhost:1337/api/'
        if not api_url.endswith('/'):
            api_url = api_url + '/'
        connector = connector or DefaultConnectorSync()
        self._connector = ConnectorWrapperSync(api_url, connector)
        self._token = token

    def set_token(self, token: str) -> None:
        self._token = token

    @property
    def api_url(self) -> str:
        return self._connector.api_url

    def authorize(self, *, identifier: str, password: str) -> None:
        """Set up or retrieve access token.

        See https://docs.strapi.io/developer-docs/latest/guides/auth-request.html

        Usage:
        >>> client.authorize(identifier='author@strapi.io', password='strapi')
        """
        endpoint = 'auth/local'
        body = {'identifier': identifier, 'password': password}
        res_obj: StrapiAuthResponse = self._connector.post(endpoint, reqargs=dict(data=body))
        if 'jwt' in res_obj and res_obj['jwt']:
            self._token = res_obj['jwt']
        else:
            raise StrapiError(f'No JWT token in response {res_obj}')

    def get_entry(
        self,
        plural_api_id: str,
        document_id: int,
        populate: Optional[PopulationParameter] = None,
        fields: Optional[List[str]] = None,
    ) -> StrapiEntryResponse:
        """Get one entry by id.

        Usage:
        >>> client.get_entry('posts', 123)
        >>> client.get_entry('posts', 123, populate='*')
        >>> client.get_entry('posts', 123, fields=['description'])
        """
        populate_param = _stringify_parameters('populate', populate)
        fields_param = _stringify_parameters('fields', fields)
        params = {**populate_param, **fields_param}
        endpoint = f'{plural_api_id}/{document_id}'
        res: StrapiEntryResponse = self._connector.get(
            endpoint, reqargs=dict(headers=self._get_auth_header(), params=params))
        return res

    def get_entries(
        self,
        plural_api_id: str,
        sort: Optional[List[str]] = None,
        filters: Optional[dict] = None,
        populate: Optional[PopulationParameter] = None,
        fields: Optional[List[str]] = None,
        pagination: Optional[PaginationParameter] = None,
        publication_state: Optional[Union[str, PublicationState]] = None,
        get_all: bool = False,
        batch_size: int = 100,
    ) -> StrapiEntriesResponse:
        """Get list of entries.
        Optionally can operate in batch mode (if get_all is True) to get all entries with pagination

        Usage:
        >>> client.get_entries('posts')
        >>> client.get_entries('posts', get_all=True)
        >>> client.get_entries('disks', sort=['name'])
        >>> client.get_entries('disks', sort=['name:desc'])
        >>> client.get_entries('posts', filters={'name': {'$eq': 'The Name'}})
        >>> client.get_entries('posts', filters={'name': {Filter.eq: 'The Name'}})
        >>> client.get_entries('posts', populate='*')
        >>> client.get_entries('posts', populate=['colors', 'author'])
        >>> client.get_entries('posts', populate={'colors': {'populate': 'colorAnimation'}, 'author': '*'})
        >>> client.get_entries('posts', fields=['description'])
        >>> client.get_entries('posts', pagination={'limit': 3})
        >>> client.get_entries('posts', publication_state=PublicationState.preview)

        Note: Pagination methods can not be mixed. Don't use `get_all` with `pagination`.
        """
        sort_param = _stringify_parameters('sort', sort)
        filters_param = _stringify_parameters('filters', filters)
        populate_param = _stringify_parameters('populate', populate)
        fields_param = _stringify_parameters('fields', fields)
        pagination_param = _stringify_parameters('pagination', pagination) if not get_all else {}
        publication_state_param = _stringify_parameters('publicationState', publication_state)
        endpoint = plural_api_id
        params = {
            **sort_param,
            **filters_param,
            **pagination_param,
            **populate_param,
            **fields_param,
            **publication_state_param,
        }
        if not get_all:
            res: StrapiEntriesResponse = self._connector.get(
                endpoint, reqargs=dict(headers=self._get_auth_header(), params=params))
            return res
        else:
            with requests.Session() as session:
                page = 1
                get_more = True
                while get_more:
                    pagination = {'page': page, 'pageSize': batch_size}
                    pagination_param = _stringify_parameters('pagination', pagination)
                    for key in pagination_param:
                        params[key] = pagination_param[key]
                    res_obj1: StrapiEntriesResponse = self._connector.get(
                        endpoint, session=session, reqargs=dict(headers=self._get_auth_header(), params=params)
                    )
                    res_obj: StrapiEntriesResponse
                    if page == 1:
                        res_obj = res_obj1
                    else:
                        if res_obj['data'] is not None and res_obj1['data'] is not None:
                            res_obj['data'] += res_obj1['data']
                        res_obj['meta'] = res_obj1['meta']
                    page += 1
                    pages = res_obj['meta']['pagination']['pageCount']
                    get_more = page <= pages
                return res_obj

    def create_entry(self, plural_api_id: str, data: dict) -> StrapiEntryResponse:
        """Create new entry.

        Usage:
        >>> client.create_entry('posts', {'name': 'The Name'})
        """
        body = {'data': data}
        res: StrapiEntryResponse = self._connector.post(
            plural_api_id, reqargs=dict(headers=self._get_auth_header(), json=body))
        return res

    def update_entry(self, plural_api_id: str, document_id: int, data: dict) -> StrapiEntryResponse:
        """Update entry fields.

        Usage:
        >>> client.update_entry('posts', 123, {'name': 'New Name'})
        """
        endpoint = f'{plural_api_id}/{document_id}'
        body = {'data': data}
        res: StrapiEntryResponse = self._connector.put(
            endpoint, reqargs=dict(headers=self._get_auth_header(), json=body))
        return res

    def delete_entry(self, plural_api_id: str, document_id: int) -> StrapiEntryResponse:
        """Delete entry by id.

        Usage:
        >>> client.delete_entry('posts', 123)
        """
        endpoint = f'{plural_api_id}/{document_id}'
        res: StrapiEntryResponse = self._connector.delete(endpoint, reqargs=dict(headers=self._get_auth_header()))
        return res

    def upsert_entry(self, plural_api_id: str, data: dict, keys: List[str]) -> StrapiEntryResponse:
        """Create entry or update fields.

        Raise `ValueError` if more than one matching entry was found.

        Usage:
        >>> client.upsert_entry('posts', {'name': 'Unique Name', 'description': 'blabla'}, ['name'])
        """
        filters = {}
        for key in keys:
            filters[key] = {'$eq': data[key]}
        current_rec = self.get_entries(
            plural_api_id=plural_api_id,
            fields=['id'],
            filters=filters,
            pagination={'page': 1, 'pageSize': 2}
        )
        num = current_rec['meta']['pagination']['total']
        if num > 1:
            raise ValueError(f'Keys are ambiguous, found {num} records')
        elif num == 1:
            try:
                entry_id: int = current_rec['data'][0]['id']  # type: ignore
            except Exception:
                raise StrapiError(f"Can't parse entry id of {current_rec}") from None
            return self.update_entry(plural_api_id=plural_api_id, document_id=entry_id, data=data)
        else:
            return self.create_entry(plural_api_id=plural_api_id, data=data)

    def _get_auth_header(self) -> Optional[dict]:
        """Compose auth header from token."""
        if self._token:
            header = {'Authorization': 'Bearer ' + self._token}
        else:
            header = None
        return header
