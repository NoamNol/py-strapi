import pytest
from typing import Any, Type

from test.types import AnyStrapiClient
from pystrapi.strapi_client import StrapiClient
from pystrapi.strapi_client_sync import StrapiClientSync


@pytest.fixture(params=[StrapiClientSync, StrapiClient])
def client(request: Any) -> AnyStrapiClient:
    client_type: Type[AnyStrapiClient] = request.param
    return client_type()


@pytest.fixture
def post1() -> dict:
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
    return {
        "id": 2,
        "attributes": {
            "description": "The second post",
            "content": "Hello again",
            "title": "Second Post"
        }
    }
