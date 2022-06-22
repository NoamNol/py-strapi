from pystrapi.strapi_client_sync import StrapiClientSync


def test_api_url() -> None:
    client = StrapiClientSync(api_url='url/')
    assert client.api_url == 'url/'


def test_api_url_no_slash() -> None:
    client = StrapiClientSync(api_url='url')
    assert client.api_url == 'url/'
