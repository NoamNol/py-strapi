from typing import Any, Dict, Iterator, List, Mapping, Optional, Tuple, Type, Union

from pystrapi.errors import (
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    RatelimitError,
    StrapiError,
    ValidationError
)
from pystrapi.types import (
    StrapiEntryOrEntriesResponse,
    StrapiResponseMessage,
    StrapiResponse,
    StrapiResponseEntryData,
    StrapiResponseError,
    StrapiResponseMetaPagination
)


def _add_id_to_attributes(entry: StrapiResponseEntryData) -> Dict[str, Any]:
    return {'id': entry['id'], **entry['attributes']}


def process_data(response: Union[Mapping, dict]) -> Union[dict, List[dict]]:
    """Process response with entries.

    Usage:
    >>> process_data(sync_client.get_entry('posts', 1))
    {'id': 1, 'name': 'post1', 'description': '...'}

    >>> process_data(sync_client.get_entries('posts'))
    [
        {'id': 1, 'name': 'post1', 'description': '...'},
        {'id': 2, 'name': 'post2', 'description': '...'},
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


def process_response(response: Union[Mapping, dict]) -> Tuple[Union[dict, List[dict]], StrapiResponseMetaPagination]:
    """Process response with entries."""
    response: StrapiEntryOrEntriesResponse = response  # type: ignore
    entries = process_data(response)
    pagination = response['meta']['pagination']
    return entries, pagination


def _stringify_parameters(name: str, parameters: Union[str, Mapping, List[str], None]) -> Dict[str, Any]:
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


def get_response_messages(response: StrapiResponse) -> List[StrapiResponseMessage]:
    messages: List[StrapiResponseMessage] = []
    for messages_group in response.get('message', []):  # type: ignore
        for message in messages_group.get('messages', []):
            if 'message' in message and 'id' in message:
                messages.append(message)
    return messages


def raise_for_strapi_response(response: StrapiResponse, status_code: int, action: str) -> None:
    """Raise suitable Strapi exception if response status code is above (or equal to) 400."""
    if status_code < 400:
        return
    message = f'Unable to {action}, status code: {status_code}, response: {response}'
    error: Optional[StrapiResponseError] = response.get('error')
    if error:
        error_name: str = error['name']
        map_exceptions: Dict[str, Type[StrapiError]] = {
            'ForbiddenError': ForbiddenError,
            'InternalServerError': InternalServerError,
            'NotFoundError': NotFoundError,
            'ValidationError': ValidationError,
        }
        if error_name in map_exceptions:
            exception_type = map_exceptions[error_name]
            raise exception_type(message)
    messages = get_response_messages(response)
    for msg in messages:
        if 'ratelimit' in msg['id']:
            raise RatelimitError(message)
    raise StrapiError(message)
