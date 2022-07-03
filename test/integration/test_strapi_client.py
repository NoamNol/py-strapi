import pytest
from pydash.predicates import is_match  # type: ignore

from test.types import AnyStrapiClient
from test.utils.asyncutils import asvalue
from pystrapi import errors
from pystrapi.types import StrapiEntriesResponse, StrapiEntryResponse


def _assert_entry_attrs_match(res: StrapiEntryResponse, entry_attrs: dict) -> None:
    assert res['data']
    assert is_match(res['data']['attributes'], entry_attrs)


async def _delete_entry_if_exists(
    auth_client: AnyStrapiClient, plural_api_id: str, entry_attrs: dict, key: str
) -> None:
    find_res: StrapiEntriesResponse = await asvalue(
        auth_client.get_entries(plural_api_id, filters={key: {'$eq': entry_attrs[key]}}))
    if find_res['data']:
        assert len(find_res['data']) == 1
        await asvalue(auth_client.delete_entry(plural_api_id, find_res['data'][0]['id']))


async def test_get_entry(client: AnyStrapiClient, post1: dict) -> None:
    res: StrapiEntryResponse = await asvalue(client.get_entry('posts', 1))
    assert is_match(res['data'], post1)


async def test_get_entry__not_found(client: AnyStrapiClient) -> None:
    bad_id = -1
    with pytest.raises(errors.NotFoundError):
        await asvalue(client.get_entry('posts', bad_id))


async def test_get_entries(client: AnyStrapiClient, post1: dict, post2: dict) -> None:
    res: StrapiEntriesResponse = await asvalue(client.get_entries('posts'))
    assert res['data']
    assert is_match(res['data'][0], post1)
    assert is_match(res['data'][1], post2)


async def test_create_and_delete_entry(auth_client: AnyStrapiClient, post3_attrs: dict) -> None:
    # TODO: split into smaller functions when db reset between tests is implemented
    await _delete_entry_if_exists(auth_client, 'posts', post3_attrs, 'title')  # First, delete leftovers

    create_res: StrapiEntryResponse = await asvalue(auth_client.create_entry('posts', post3_attrs))
    assert create_res['data']
    assert is_match(create_res['data']['attributes'], post3_attrs)
    get_res: StrapiEntryResponse = await asvalue(auth_client.get_entry('posts', create_res['data']['id']))
    assert get_res['data']
    assert is_match(get_res['data']['attributes'], post3_attrs)
    delete_res: StrapiEntryResponse = await asvalue(
        auth_client.delete_entry('posts', create_res['data']['id']))
    assert delete_res['data']
    assert is_match(delete_res['data']['attributes'], post3_attrs)
    find_deleted_res: StrapiEntriesResponse = await asvalue(
        auth_client.get_entries('posts', filters={'title': {'$eq': post3_attrs['title']}}))
    assert not find_deleted_res['data']  # No data because deleted not found


async def test_delete_entry__forbidden(client: AnyStrapiClient) -> None:
    """Can't delete if client isn't authorized"""
    with pytest.raises(errors.ForbiddenError):
        await asvalue(client.delete_entry('posts', 2))


async def test_update_entry__all_fields(auth_client: AnyStrapiClient, post3_attrs: dict) -> None:
    await _delete_entry_if_exists(auth_client, 'posts', post3_attrs, 'title')

    create_res: StrapiEntryResponse = await asvalue(auth_client.create_entry('posts', post3_attrs))
    assert create_res['data']
    entry_id = create_res['data']['id']
    new_data = {**post3_attrs, **{'content': 'new content'}}
    update_res: StrapiEntryResponse = await asvalue(auth_client.update_entry('posts', entry_id, new_data))
    _assert_entry_attrs_match(update_res, new_data)
    get_res: StrapiEntryResponse = await asvalue(auth_client.get_entry('posts', entry_id))
    _assert_entry_attrs_match(get_res, new_data)


async def test_update_entry__one_field(auth_client: AnyStrapiClient, post3_attrs: dict) -> None:
    await _delete_entry_if_exists(auth_client, 'posts', post3_attrs, 'title')

    new_data = {'content': 'new content-2'}
    create_res: StrapiEntryResponse = await asvalue(auth_client.create_entry('posts', post3_attrs))
    assert create_res['data']
    entry_id = create_res['data']['id']
    update_res: StrapiEntryResponse = await asvalue(
        auth_client.update_entry('posts', entry_id, new_data))
    _assert_entry_attrs_match(update_res, new_data)
    get_res: StrapiEntryResponse = await asvalue(auth_client.get_entry('posts', entry_id))
    _assert_entry_attrs_match(get_res, new_data)


async def test_update_entry__validation_error(auth_client: AnyStrapiClient, post1: dict, post2: dict) -> None:
    # (Post title is defined as a unique field in the database)
    post2_title = post2['attributes']['title']
    with pytest.raises(errors.ValidationError):
        await asvalue(auth_client.update_entry('posts', post1['id'], {'title': post2_title}))
