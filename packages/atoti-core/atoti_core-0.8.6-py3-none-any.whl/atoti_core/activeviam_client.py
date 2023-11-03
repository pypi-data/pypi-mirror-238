from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from email.message import Message
from functools import cached_property
from http.client import HTTPResponse
from pathlib import Path
from ssl import create_default_context
from typing import (
    IO,
    Any,
    Literal,
    NoReturn,
    Optional,
    TypedDict,
    Union,
    cast,
    overload,
)
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import (
    AbstractHTTPHandler,
    BaseHandler,
    HTTPDefaultErrorHandler,
    HTTPSHandler,
    Request,
    build_opener,
)

from typing_extensions import TypeGuard, override

from ._get_endpoint_path import get_endpoint_path
from ._server_versions import ServerVersions
from .fetch_json import JSON_CONTENT_TYPE, JsonResponse, fetch_json
from .http_method import HttpMethod
from .path import local_to_absolute_path


class _ErrorChainItem(TypedDict):
    message: str
    type: str


class _CurrentActiveViamJsonHttpErrorBody(TypedDict):
    errorChain: Sequence[_ErrorChainItem]
    stackTrace: str


class _LegacyActiveViamJsonHttpErrorBody(TypedDict):  # Atoti Server < 6.0.0-M1.
    error: _CurrentActiveViamJsonHttpErrorBody
    status: Literal["error"]


def _is_current_activeviam_json_http_error_body(
    body: Any,
) -> TypeGuard[_CurrentActiveViamJsonHttpErrorBody]:
    return (
        isinstance(body, dict)
        and "errorChain" in body
        and isinstance(body["errorChain"], list)
        and "stackTrace" in body
        and isinstance(body["stackTrace"], str)
    )


def _is_legacy_activeviam_json_http_error_body(
    body: Any, /
) -> TypeGuard[_LegacyActiveViamJsonHttpErrorBody]:
    return (
        isinstance(body, dict)
        and body.get("status") == "error"
        and _is_current_activeviam_json_http_error_body(body.get("error"))
    )


def parse_error_body(body: Any) -> _CurrentActiveViamJsonHttpErrorBody:
    if _is_current_activeviam_json_http_error_body(body):
        return body

    if _is_legacy_activeviam_json_http_error_body(body):
        return body["error"]

    return {"errorChain": [], "stackTrace": str(body)}


class ActiveViamHttpError(HTTPError):
    def __init__(
        self,
        *,
        body: _CurrentActiveViamJsonHttpErrorBody,
        code: int,
        hdrs: Message,  # spell-checker: disable-line
        url: str,
    ) -> None:
        super().__init__(
            url,
            code,
            body["stackTrace"],
            hdrs,  # spell-checker: disable-line
            None,
        )

        self.error_chain: Sequence[_ErrorChainItem] = body["errorChain"]


class _ActiveViamJsonHttpErrorHandler(HTTPDefaultErrorHandler):
    @override
    def http_error_default(  # pylint: disable=too-many-positional-parameters
        self,
        req: Request,
        fp: Optional[IO[bytes]],
        code: int,
        msg: str,
        hdrs: Message,  # spell-checker: disable-line
    ) -> NoReturn:
        error = HTTPError(
            req.full_url,
            code,
            msg,
            hdrs,  # spell-checker: disable-line
            fp,
        )

        if fp is None or (
            hdrs.get_content_type() != JSON_CONTENT_TYPE  # spell-checker: disable-line
        ):
            raise error

        body = json.load(fp)
        parsed_body = parse_error_body(body)

        raise ActiveViamHttpError(
            body=parsed_body,
            code=code,
            hdrs=hdrs,  # spell-checker: disable-line
            url=req.full_url,
        ) from error


_Auth = Callable[[str], Mapping[str, str]]


class _AuthHandler(AbstractHTTPHandler):
    def __init__(self, auth: _Auth, /) -> None:
        super().__init__()

        self._auth = auth

    def _handle_request(self, request: Request) -> Request:
        headers = self._auth(request.full_url)
        request.headers.update(headers)
        return request

    http_request = _handle_request
    https_request = _handle_request


class ActiveViamClient:
    """Used to communicate with ActiveViam servers such as Atoti Server or the Content Server.

    This class uses a custom HTTP error handler to enrich the raised errors with the server stack trace.
    """

    def __init__(
        self,
        url: str,
        /,
        *,
        auth: Optional[_Auth] = None,
        certificate_authority: Optional[Path] = None,
        client_certificate: Optional[Path] = None,
        client_certificate_keyfile: Optional[Path] = None,
        client_certificate_password: Optional[str] = None,
    ) -> None:
        self._url = url.strip("/")

        handlers: list[BaseHandler] = [_ActiveViamJsonHttpErrorHandler()]

        if auth:
            handlers.append(_AuthHandler(auth))

        if certificate_authority or client_certificate:
            context = create_default_context()
            if certificate_authority:
                context.load_verify_locations(
                    cafile=local_to_absolute_path(certificate_authority)
                )
            if client_certificate:
                context.load_cert_chain(
                    certfile=local_to_absolute_path(client_certificate),
                    keyfile=local_to_absolute_path(client_certificate_keyfile)
                    if client_certificate_keyfile
                    else None,
                    password=client_certificate_password,
                )
            handlers.append(HTTPSHandler(context=context))

        self._opener_director = build_opener(*handlers)

    @property
    def url(self) -> str:
        return self._url

    @overload
    def fetch_json(
        self,
        *,
        body: object = ...,
        method: Optional[HttpMethod] = ...,
        namespace: str,
        query: str = ...,
        raw: Literal[True],
        route: str,
    ) -> HTTPResponse:
        ...

    @overload
    def fetch_json(
        self,
        *,
        body: object = ...,
        method: Optional[HttpMethod] = ...,
        namespace: str,
        query: str = ...,
        raw: Literal[False] = ...,
        route: str,
    ) -> JsonResponse:
        ...

    def fetch_json(
        self,
        *,
        body: object = None,
        method: Optional[HttpMethod] = None,
        namespace: str,
        query: str = "",
        raw: bool = False,
        route: str,
    ) -> Union[JsonResponse, HTTPResponse]:
        url = self._get_endpoint_url(namespace=namespace, route=route)

        if query:
            url = f"{url}?{query}"

        response = fetch_json(
            url,
            body=body,
            method=method,
            opener_director=self._opener_director,
            raw=raw,
        )

        if raw:
            return response

        assert isinstance(response, JsonResponse)

        if (
            isinstance(response.body, dict)
            and "data" in response.body
            and response.body.get("status") == "success"
        ):
            # Atoti Server < 6.0.0-M1.
            return replace(response, body=response.body["data"])

        return response

    def ping(self) -> str:
        url = self._get_endpoint_url(namespace="activeviam/pivot", route="ping")
        response = self._opener_director.open(url)
        body = cast(str, response.read().decode("utf8"))
        expected_body = "pong"
        if body != expected_body:
            raise RuntimeError(
                f"Expected `ping()`'s response body to be `{expected_body}` but got `{body}`."
            )
        return body

    def _get_endpoint_path(
        self,
        *,
        attribute_name: Literal["restPath", "wsPath"] = "restPath",
        namespace: str,
        route: str,
    ) -> str:
        return get_endpoint_path(
            attribute_name=attribute_name,
            namespace=namespace,
            route=route,
            server_versions=self.server_versions,
        )

    def _get_url(self, path: str, /) -> str:
        return urljoin(f"{self.url}/", path.lstrip("/"))

    def _get_endpoint_url(
        self,
        *,
        attribute_name: Literal["restPath", "wsPath"] = "restPath",
        namespace: str,
        route: str,
    ) -> str:
        path = self._get_endpoint_path(
            attribute_name=attribute_name, namespace=namespace, route=route
        )
        return self._get_url(path)

    @cached_property
    def server_versions(self) -> ServerVersions:
        url = self._get_url("versions/rest")
        body = fetch_json(url, opener_director=self._opener_director).body
        return cast(ServerVersions, body)

    @property
    def has_atoti_python_api_endpoints(self) -> bool:
        return "atoti" in self.server_versions["apis"]
