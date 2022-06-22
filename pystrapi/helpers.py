from typing import Any, Dict, Iterator, List, Mapping, Tuple, Union

from .types import StrapiEntryOrEntriesResponse, StrapiResponseEntryData, StrapiResponseMetaPagination


def _add_id_to_attributes(entry: StrapiResponseEntryData) -> Dict[str, Any]:
    return {"id": entry["id"], **entry["attributes"]}


def process_data(response: dict) -> Union[dict, List[dict]]:
    """Process response with entries.

    Usage:
    >>> process_data(sync_client.get_entry('posts', 1))
    {"id": 1, "name": "post1", "description": "..."}

    >>> process_data(sync_client.get_entries('posts'))
    [
        {"id": 1, "name": "post1", "description": "..."},
        {"id": 2, "name": "post2", "description": "..."},
    ]
    """
    response: StrapiEntryOrEntriesResponse = response  # type: ignore
    if not response['data']:
        return []
    data = response['data']
    if isinstance(data, list):
        return [_add_id_to_attributes(d) for d in data]
    else:
        return _add_id_to_attributes(data)


def process_response(response: dict) -> Tuple[Union[dict, List[dict]], StrapiResponseMetaPagination]:
    """Process response with entries"""
    response: StrapiEntryOrEntriesResponse = response  # type: ignore
    entries = process_data(response)
    pagination = response['meta']['pagination']
    return entries, pagination


def _stringify_parameters(name: str, parameters: Union[str, Mapping, List[str], None]) -> Dict[str, Any]:
    """Stringify dict for query parameters"""
    if isinstance(parameters, dict):
        return {name + k: v for k, v in _flatten_parameters(parameters)}
    elif isinstance(parameters, str):
        return {name: parameters}
    elif isinstance(parameters, list):
        return {name: ','.join(parameters)}
    else:
        return {}


def _flatten_parameters(parameters: dict) -> Iterator[Tuple[str, Any]]:
    """Flatten parameters dict for query"""
    for key, value in parameters.items():
        if isinstance(value, dict):
            for key1, value1 in _flatten_parameters(value):
                yield f'[{key}]{key1}', value1
        else:
            yield f'[{key}]', value
