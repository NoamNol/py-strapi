from pystrapi.strapi_client_sync import StrapiClientSync


def test_baseurl() -> None:
    client = StrapiClientSync(baseurl='url/')
    assert client.baseurl == 'url/'


def test_baseurl_no_slash() -> None:
    client = StrapiClientSync(baseurl='url')
    assert client.baseurl == 'url/'
