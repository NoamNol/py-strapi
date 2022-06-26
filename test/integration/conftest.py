# pylint: disable=redefined-outer-name

import pytest
from typing import Any, Type

from test.types import AnyStrapiClient
from test.utils.asyncutils import asvalue
from pystrapi.strapi_client import StrapiClient
from pystrapi.strapi_client_sync import StrapiClientSync


@pytest.fixture(params=[StrapiClientSync, StrapiClient])
def client(request: Any) -> AnyStrapiClient:
    client_type: Type[AnyStrapiClient] = request.param
    return client_type()


@pytest.fixture
async def auth_client(client: AnyStrapiClient) -> AnyStrapiClient:
    await asvalue(client.authorize(identifier='strapi1@test.com', password='strapi'))  # nosec
    return client


@pytest.fixture
def post1() -> dict:
    """This post should already be in test-db"""
    return {
        "id": 1,
        "attributes": {
            "description": "The first post",
            "content": "Hello",
            "title": "First Post",
        }
    }


@pytest.fixture
def post2() -> dict:
    """This post should already be in test-db"""
    return {
        "id": 2,
        "attributes": {
            "description": "The second post",
            "content": "Hello again",
            "title": "Second Post"
        }
    }


@pytest.fixture
def post3_attrs() -> dict:
    """This post should not be in test-db at the beginning"""
    return {
        "description": "The third post",
        "content": "Hello",
        "title": "Third Post"
    }
