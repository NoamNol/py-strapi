from pystrapi.strapi_client import StrapiClient


def test_api_url() -> None:
    client = StrapiClient(api_url='url/')
    assert client.api_url == 'url/'


def test_api_url_no_slash() -> None:
    client = StrapiClient(api_url='url')
    assert client.api_url == 'url/'
