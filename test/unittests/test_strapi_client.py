from pystrapi.strapi_client import StrapiClient


def test_baseurl() -> None:
    client = StrapiClient('url/')
    assert client.baseurl == 'url/'


def test_baseurl_no_slash() -> None:
    client = StrapiClient('url')
    assert client.baseurl == 'url/'
