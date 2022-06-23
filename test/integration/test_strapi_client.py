from test.types import AnyStrapiClient
from test.utils import asyncutils
from pystrapi.types import StrapiEntriesResponse, StrapiEntryResponse

from pydash.predicates import is_match  # type: ignore


async def test_get_entry(client: AnyStrapiClient, post1: dict) -> None:
    res: StrapiEntryResponse = await asyncutils.value(client.get_entry('posts', 1))
    assert is_match(res['data'], post1)


async def test_get_entries(client: AnyStrapiClient, post1: dict, post2: dict) -> None:
    res: StrapiEntriesResponse = await asyncutils.value(client.get_entries('posts'))
    assert res['data']
    assert is_match(res['data'][0], post1)
    assert is_match(res['data'][1], post2)
