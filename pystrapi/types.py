from typing import Any, Dict, List, Optional, Union
from typing_extensions import TypedDict, NotRequired


# ------------------- RESPONSE TYPES -------------------

class StrapiResponseEntryData(TypedDict):
    id: int
    attributes: Dict[str, Any]
    meta: NotRequired[dict]


class StrapiResponseMetaPagination(TypedDict):
    page: int
    pageSize: int
    pageCount: int
    total: int


class StrapiResponseMeta(TypedDict):
    pagination: NotRequired[StrapiResponseMetaPagination]


class StrapiResponseError(TypedDict):
    status: int
    name: str
    message: str
    details: dict


class StrapiResponseMessage(TypedDict):
    id: str
    message: str


class StrapiResponseMessagesGroup(TypedDict):
    messages: List[StrapiResponseMessage]


class StrapiEntryResponse(TypedDict):
    data: Optional[StrapiResponseEntryData]
    meta: NotRequired[StrapiResponseMeta]
    error: NotRequired[StrapiResponseError]


class StrapiEntriesResponse(TypedDict):
    data: Optional[List[StrapiResponseEntryData]]
    meta: NotRequired[StrapiResponseMeta]
    error: NotRequired[StrapiResponseError]


StrapiEntryOrEntriesResponse = Union[StrapiEntryResponse, StrapiEntriesResponse]


class StrapiResponseUser(TypedDict):
    id: int
    username: str


class StrapiAuthResponse(TypedDict):
    jwt: str
    user: StrapiResponseUser
    data: NotRequired[Any]
    error: NotRequired[StrapiResponseError]
    message: NotRequired[List[StrapiResponseMessagesGroup]]


StrapiResponse = Union[StrapiEntryResponse, StrapiEntriesResponse, StrapiAuthResponse]


# ------------------- PARAMETER TYPES -------------------

class PaginationParameterByPage(TypedDict):
    page: NotRequired[int]
    pageSize: NotRequired[int]
    withCount: NotRequired[bool]


class PaginationParameterByOffset(TypedDict):
    start: NotRequired[int]
    limit: NotRequired[int]
    withCount: NotRequired[bool]


PaginationParameter = Union[PaginationParameterByPage, PaginationParameterByOffset]
PopulationParameter = Union[str, List[str], Dict[str, Any]]
