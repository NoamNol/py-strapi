from typing import Optional, List, Union
import aiohttp

from .parameters import PublicationState
from .types import PaginationParameter, PopulationParameter, StrapiEntriesResponse, StrapiEntryResponse
from .helpers import _stringify_parameters


class StrapiClient:
    """REST API client for Strapi.

    Strapi docs:
    https://docs.strapi.io/developer-docs/latest/developer-resources/database-apis-reference/rest-api.html
    """

    def __init__(
        self, *,
        api_url: Optional[str] = None,
        token: Optional[str] = None
    ):
        api_url = api_url or "http://localhost:1337/api/"
        if not api_url.endswith('/'):
            api_url = api_url + '/'
        self.api_url: str = api_url
        self._token: Optional[str] = token

    def set_token(self, token: str) -> None:
        self._token = token

    async def authorize(self, *, identifier: str, password: str) -> None:
        """Set up or retrieve access token.

        See https://docs.strapi.io/developer-docs/latest/guides/auth-request.html

        Usage:
        >>> client.authorize(identifier="author@strapi.io", password="strapi")
        """
        url = self.api_url + 'api/auth/local'
        body = {
            'identifier': identifier,
            'password': password
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as res:
                if res.status != 200:
                    raise Exception(f'Unable to authorize, error {res.status}: {res.reason}')
                res_obj = await res.json()
                if 'jwt' in res_obj and res_obj['jwt']:
                    self._token = res_obj['jwt']
                else:
                    raise Exception('No JWT token in response')

    async def get_entry(
        self,
        plural_api_id: str,
        document_id: int,
        populate: Optional[PopulationParameter] = None,
        fields: Optional[List[str]] = None
    ) -> StrapiEntryResponse:
        """Get one entry by id.

        Usage:
        >>> client.get_entry('posts', 123)
        >>> client.get_entry('posts', 123, populate="*")
        >>> client.get_entry('posts', 123, fields=["description"])
        """
        populate_param = _stringify_parameters('populate', populate)
        fields_param = _stringify_parameters('fields', fields)
        params = {
            **populate_param,
            **fields_param
        }
        url = f'{self.api_url}api/{plural_api_id}/{document_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._get_auth_header(), params=params) as res:
                if res.status != 200:
                    raise Exception(f'Unable to get entry, error {res.status}: {res.reason}')
                return await res.json()  # type: ignore

    async def get_entries(
        self,
        plural_api_id: str,
        sort: Optional[List[str]] = None,
        filters: Optional[dict] = None,
        populate: Optional[PopulationParameter] = None,
        fields: Optional[List[str]] = None,
        pagination: Optional[PaginationParameter] = None,
        publication_state: Optional[Union[str, PublicationState]] = None,
        get_all: bool = False,
        batch_size: int = 100
    ) -> StrapiEntriesResponse:
        """Get list of entries.
        Optionally can operate in batch mode (if get_all is True) to get all entries with pagination

        Usage:
        >>> client.get_entries('posts')
        >>> client.get_entries('posts', get_all=True)
        >>> client.get_entries('disks', sort=["name"])
        >>> client.get_entries('disks', sort=["name:desc"])
        >>> client.get_entries('posts', filters={"name": {"$eq": "The Name"}})
        >>> client.get_entries('posts', filters={"name": {Filter.eq: "The Name"}})
        >>> client.get_entries('posts', populate="*")
        >>> client.get_entries('posts', populate=["colors", "author"])
        >>> client.get_entries('posts', populate={"colors": {"populate": "colorAnimation"}, "author": "*"})
        >>> client.get_entries('posts', fields=["description"])
        >>> client.get_entries('posts', pagination={"limit": 3})
        >>> client.get_entries('posts', publication_state=PublicationState.preview)
        """
        sort_param = _stringify_parameters('sort', sort)
        filters_param = _stringify_parameters('filters', filters)
        populate_param = _stringify_parameters('populate', populate)
        fields_param = _stringify_parameters('fields', fields)
        pagination_param = _stringify_parameters('pagination', pagination)
        publication_state_param = _stringify_parameters('publicationState', publication_state)
        url = f'{self.api_url}api/{plural_api_id}'
        params = {
            **sort_param,
            **filters_param,
            **pagination_param,
            **populate_param,
            **fields_param,
            **publication_state_param
        }
        async with aiohttp.ClientSession() as session:
            res_obj: StrapiEntriesResponse
            if not get_all:
                res_obj = await self._get_entries(session, url, params)
                return res_obj
            else:
                page = 1
                get_more = True
                while get_more:
                    pagination = {
                        'page': page,
                        'pageSize': batch_size
                    }
                    pagination_param = _stringify_parameters('pagination', pagination)
                    for key in pagination_param:
                        params[key] = pagination_param[key]
                    res_obj1 = await self._get_entries(session, url, params)
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

    async def create_entry(self, plural_api_id: str, data: dict) -> StrapiEntryResponse:
        """Create new entry.

        Usage:
        >>> client.create_entry("posts", {"name": "The Name"})
        """
        url = f'{self.api_url}api/{plural_api_id}'
        body = {
            'data': data
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=self._get_auth_header()) as res:
                if res.status != 200:
                    raise Exception(f'Unable to create entry, error {res.status}: {res.reason}')
                return await res.json()  # type: ignore

    async def update_entry(
        self,
        plural_api_id: str,
        document_id: int,
        data: dict
    ) -> StrapiEntryResponse:
        """Update entry fields.

        Usage:
        >>> client.update_entry("posts", 123, {"name": "New Name"})
        """
        url = f'{self.api_url}api/{plural_api_id}/{document_id}'
        body = {
            'data': data
        }
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=body, headers=self._get_auth_header()) as res:
                if res.status != 200:
                    raise Exception(f'Unable to update entry, error {res.status}: {res.reason}')
                return await res.json()  # type: ignore

    async def delete_entry(self, plural_api_id: str, document_id: int) -> StrapiEntryResponse:
        """Delete entry by id.

        Usage:
        >>> client.delete_entry("posts", 123)
        """
        url = f'{self.api_url}api/{plural_api_id}/{document_id}'
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self._get_auth_header()) as res:
                if res.status != 200:
                    raise Exception(f'Unable to delete entry, error {res.status}: {res.reason}')
                return await res.json()  # type: ignore

    async def upsert_entry(
        self,
        plural_api_id: str,
        data: dict,
        keys: List[str]
    ) -> StrapiEntryResponse:
        """Create entry or update fields.

        Raise `ValueError` if more than one matching entry was found.

        Usage:
        >>> client.upsert_entry('posts', {"name": "Unique Name", "description": "blabla"}, ['name'])
        """
        filters = {}
        for key in keys:
            filters[key] = {'$eq': data[key]}
        current_rec = await self.get_entries(
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
                raise Exception(f"Can't parse entry id of {current_rec}") from None
            return await self.update_entry(
                plural_api_id=plural_api_id,
                document_id=entry_id,
                data=data
            )
        else:
            return await self.create_entry(
                plural_api_id=plural_api_id,
                data=data
            )

    def _get_auth_header(self) -> Optional[dict]:
        """Compose auth header from token."""
        if self._token:
            header = {'Authorization': 'Bearer ' + self._token}
        else:
            header = None
        return header

    async def _get_entries(self, session: aiohttp.ClientSession, url: str, params: dict) -> StrapiEntriesResponse:
        """Helper function to get entries."""
        async with session.get(
                url,
                headers=self._get_auth_header(),
                params=params
        ) as res:
            if res.status != 200:
                raise Exception(f'Unable to get entries, error {res.status}: {res.reason}')
            res_obj = await res.json()
            return res_obj  # type: ignore
