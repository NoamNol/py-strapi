import requests
from typing import List, Optional

from .helpers import _stringify_parameters
from .strapi_connector_sync import DefaultStrapiConnectorSync, StrapiConnectorSync


class StrapiClientSync:
    """RESP API client for Strapi."""

    def __init__(
        self, *,
        baseurl: Optional[str] = None,
        connector: Optional[StrapiConnectorSync] = None,
        token: Optional[str] = None,
    ):
        """Initialize client."""
        baseurl = baseurl or "http://localhost:1337/api/"
        if not baseurl.endswith('/'):
            baseurl = baseurl + '/'
        self._connector = connector or DefaultStrapiConnectorSync(baseurl)
        self._token = token

    def set_token(self, token: str) -> None:
        self._token = token

    @property
    def baseurl(self) -> str:
        return self._connector.api_url

    def authorize(self, *, identifier: str, password: str) -> None:
        """Set up or retrieve access token."""
        endpoint = "auth/local"
        body = {"identifier": identifier, "password": password}
        res_obj = self._connector.post(endpoint, reqargs=dict(data=body))
        self._token = res_obj["jwt"]

    def get_entry(
            self,
            plural_api_id: str,
            document_id: int,
            populate: Optional[List[str]] = None,
            fields: Optional[List[str]] = None
    ) -> dict:
        """Get entry by id."""
        populate_param = _stringify_parameters("populate", populate)
        fields_param = _stringify_parameters("fields", fields)
        params = {**populate_param, **fields_param}
        endpoint = f"{plural_api_id}/{document_id}"
        res: dict = self._connector.get(endpoint, reqargs=dict(headers=self._get_auth_header(), params=params))
        return res

    def get_entries(
            self,
            plural_api_id: str,
            sort: Optional[List[str]] = None,
            filters: Optional[dict] = None,
            populate: Optional[List[str]] = None,
            fields: Optional[List[str]] = None,
            pagination: Optional[dict] = None,
            publication_state: Optional[str] = None,
            get_all: bool = False,
            batch_size: int = 100
    ) -> dict:
        """Get list of entries. Optionally can operate in batch mode to get all entries automatically."""
        sort_param = _stringify_parameters("sort", sort)
        filters_param = _stringify_parameters("filters", filters)
        populate_param = _stringify_parameters("populate", populate)
        fields_param = _stringify_parameters("fields", fields)
        pagination_param = _stringify_parameters("pagination", pagination)
        publication_state_param = _stringify_parameters("publicationState", publication_state)
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
            res: dict = self._connector.get(
                endpoint, reqargs=dict(headers=self._get_auth_header(), params=params))
            return res
        else:
            with requests.Session() as session:
                page = 1
                get_more = True
                while get_more:
                    pagination = {"page": page, "pageSize": batch_size}
                    pagination_param = _stringify_parameters("pagination", pagination)
                    for key in pagination_param:
                        params[key] = pagination_param[key]
                    res_obj1: dict = self._connector.get(
                        endpoint, session=session, reqargs=dict(headers=self._get_auth_header(), params=params)
                    )
                    if page == 1:
                        res_obj = res_obj1
                    else:
                        res_obj["data"] += res_obj1["data"]
                        res_obj["meta"] = res_obj1["meta"]
                    page += 1
                    pages = res_obj["meta"]["pagination"]["pageCount"]
                    get_more = page <= pages
                return res_obj

    def create_entry(
            self,
            plural_api_id: str,
            data: dict
    ) -> dict:
        body = {"data": data}
        res: dict = self._connector.post(
            plural_api_id, reqargs=dict(headers=self._get_auth_header(), json=body))
        return res

    def update_entry(
            self,
            plural_api_id: str,
            document_id: int,
            data: dict
    ) -> dict:
        """Update entry fields."""
        endpoint = f"{plural_api_id}/{document_id}"
        body = {"data": data}
        res: dict = self._connector.put(
            endpoint, reqargs=dict(headers=self._get_auth_header(), json=body))
        return res

    def delete_entry(
            self,
            plural_api_id: str,
            document_id: int
    ) -> dict:
        """Delete entry by id."""
        endpoint = f"{plural_api_id}/{document_id}"
        res: dict = self._connector.delete(endpoint, reqargs=dict(headers=self._get_auth_header()))
        return res

    def upsert_entry(
            self,
            plural_api_id: str,
            data: dict,
            keys: List[str]
    ) -> dict:
        """Create entry or update fields."""
        filters = {}
        for key in keys:
            filters[key] = {"$eq": data[key]}
        current_rec = self.get_entries(
            plural_api_id=plural_api_id,
            fields=["id"],
            filters=filters,
            pagination={"page": 1, "pageSize": 2}
        )
        num = current_rec["meta"]["pagination"]["total"]
        if num > 1:
            raise ValueError(f"Keys are ambiguous, found {num} records")
        elif num == 1:
            try:
                entry_id: int = current_rec["data"][0]["id"]
            except Exception:
                raise Exception(f"Can't parse entry id of {current_rec}") from None
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
