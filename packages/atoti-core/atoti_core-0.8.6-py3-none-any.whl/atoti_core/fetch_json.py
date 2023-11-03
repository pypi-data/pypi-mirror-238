import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import timedelta
from http.client import HTTPResponse
from mimetypes import types_map
from typing import Literal, Optional, Union, overload
from urllib.request import OpenerDirector, Request, urlopen

from .empty_mapping import EMPTY_MAPPING
from .http_method import HttpMethod
from .keyword_only_dataclass import keyword_only_dataclass

_CONTENT_TYPE_HEADER_NAME = "content-type"

JSON_CONTENT_TYPE = types_map[".json"]

_JsonDumpDefault = Callable[[object], object]

# Using `object` instead of `Any` so that callers do not forget to validate the returned body.
# See also: https://stackoverflow.com/a/51294709/5558141.
_Json = object


@keyword_only_dataclass
@dataclass(frozen=True)
class JsonResponse:
    body: _Json
    headers: Mapping[str, str]
    status_code: int


@overload
def fetch_json(
    url: str,
    /,
    *,
    body: Optional[_Json] = ...,
    headers: Mapping[str, str] = ...,
    json_dump_default: Optional[_JsonDumpDefault] = ...,
    method: Optional[HttpMethod] = ...,
    opener_director: Optional[OpenerDirector] = ...,
    timeout: Optional[timedelta] = ...,
    raw: Literal[True],
) -> HTTPResponse:
    ...


@overload
def fetch_json(
    url: str,
    /,
    *,
    body: Optional[_Json] = ...,
    headers: Mapping[str, str] = ...,
    json_dump_default: Optional[_JsonDumpDefault] = ...,
    method: Optional[HttpMethod] = ...,
    opener_director: Optional[OpenerDirector] = ...,
    timeout: Optional[timedelta] = ...,
    raw: Literal[False] = ...,
) -> JsonResponse:
    ...


@overload
def fetch_json(
    url: str,
    /,
    *,
    body: Optional[_Json] = ...,
    headers: Mapping[str, str] = ...,
    json_dump_default: Optional[_JsonDumpDefault] = ...,
    method: Optional[HttpMethod] = ...,
    opener_director: Optional[OpenerDirector] = ...,
    timeout: Optional[timedelta] = ...,
    raw: bool = ...,
) -> Union[JsonResponse, HTTPResponse]:
    ...


def fetch_json(
    url: str,
    /,
    *,
    body: Optional[_Json] = None,
    headers: Mapping[str, str] = EMPTY_MAPPING,
    json_dump_default: Optional[_JsonDumpDefault] = None,
    method: Optional[HttpMethod] = None,
    opener_director: Optional[OpenerDirector] = None,
    timeout: Optional[timedelta] = None,
    raw: bool = False,
) -> Union[JsonResponse, HTTPResponse]:
    data = (
        None
        if body is None
        else json.dumps(body, default=json_dump_default).encode("utf8")
    )
    headers = {_CONTENT_TYPE_HEADER_NAME: JSON_CONTENT_TYPE, **headers}
    request = Request(url, data=data, headers=headers, method=method)
    timeout_in_seconds = timeout.total_seconds() if timeout else None

    response: HTTPResponse = (
        opener_director.open(request, timeout=timeout_in_seconds)
        if opener_director
        else urlopen(request, timeout=timeout_in_seconds)  # noqa: S310
    )

    if raw:
        return response

    with response:
        response_content_type = response.headers.get_content_type()
        assert (
            response_content_type == JSON_CONTENT_TYPE
        ), f"Expected response's `{_CONTENT_TYPE_HEADER_NAME}` to be `{JSON_CONTENT_TYPE}` but got `{response_content_type}`."

        response_body: _Json = json.load(response)

        return JsonResponse(
            body=response_body,
            headers=dict(response.headers),
            status_code=response.status,
        )
