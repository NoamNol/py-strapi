# PyStrapi

Work with Strapi from Python via REST API

## Install

```bash
pip install pystrapi
```

## Documentation

[Full API Reference](./docs)

## Examples

Quick start:

```python
import asyncio
from pystrapi import StrapiClient

async def main():
    strapi = StrapiClient(strapi_url)
    await strapi.authorize(your_identifier, your_password) # optional
    users = await strapi.get_entries('users', filters={'username': {'$eq': 'Pavel'}})
    user_id = users['data'][0]['id']
    await strapi.update_entry('users', user_id, data={'username': 'Mark'})

asyncio.run(main())
```

## Development

### Lint
Run [prospector](https://prospector.landscape.io/):
```
prospector
```

### Create new release

Push changes to 'main' branch following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

