# PyStrapi
![CI](https://github.com/NoamNol/py-strapi/workflows/CI/badge.svg?event=push)
![Build and release](https://github.com/NoamNol/py-strapi/workflows/%F0%9F%9A%80%20Build%20and%20release/badge.svg?event=push)
[![PyPI version](https://badge.fury.io/py/pystrapi.svg)](https://pypi.org/project/pystrapi)
![pyversions](https://img.shields.io/pypi/pyversions/pystrapi)

Work with [Strapi](https://strapi.io/) from Python via REST API

## Install

```bash
pip install pystrapi
```

## Examples

Quick start:

```python
import asyncio
from pystrapi import StrapiClient

async def main():
    strapi = StrapiClient(api_url=strapi_url)
    await strapi.authorize(your_identifier, your_password) # optional
    users = await strapi.get_entries('users', filters={'username': {'$eq': 'Pavel'}})
    user_id = users['data'][0]['id']
    await strapi.update_entry('users', user_id, data={'username': 'Mark'})

asyncio.run(main())
```

## Development
### Install environment:
```
python -m venv .env
source .env/bin/activate
poetry install
```

### Lint
Run [prospector](https://prospector.landscape.io/):
```
prospector
```

### Unit tests
```
pytest test/unittests
```

### Integration tests
Run Strapi test server (see [instructions](testserver/README.md)), and run integration tests:
```
pytest test/integration
```

### Create new release

Push changes to 'main' branch following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

