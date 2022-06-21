
from typing import Any, Iterator, List, Tuple, Union


def process_data(entry: dict) -> Union[dict, List[dict]]:
    """Process response with entries."""
    data: Union[dict, List[dict]] = entry['data']
    if isinstance(data, list):
        return [{'id': d['id'], **d['attributes']} for d in data]
    else:
        return {'id': data['id'], **data['attributes']}


def process_response(response: dict) -> Tuple[Union[dict, List[dict]], dict]:
    """Process response with entries."""
    entries = process_data(response)
    pagination = response['meta']['pagination']
    return entries, pagination


def _stringify_parameters(name: str, parameters: Union[dict, List[str], str, None]) -> dict:
    """Stringify dict for query parameters."""
    if isinstance(parameters, dict):
        return {name + k: v for k, v in _flatten_parameters(parameters)}
    elif isinstance(parameters, str):
        return {name: parameters}
    elif isinstance(parameters, list):
        return {name: ','.join(parameters)}
    else:
        return {}


def _flatten_parameters(parameters: dict) -> Iterator[Tuple[str, Any]]:
    """Flatten parameters dict for query."""
    for key, value in parameters.items():
        if isinstance(value, dict):
            for key1, value1 in _flatten_parameters(value):
                yield f'[{key}]{key1}', value1
        else:
            yield f'[{key}]', value
