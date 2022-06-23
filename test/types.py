from typing import Union

from pystrapi.strapi_client import StrapiClient
from pystrapi.strapi_client_sync import StrapiClientSync

AnyStrapiClient = Union[StrapiClientSync, StrapiClient]
