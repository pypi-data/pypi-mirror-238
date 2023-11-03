from collections.abc import Mapping, Sequence
from typing import TypedDict


class _ApiVersion(TypedDict):
    id: str
    restPath: str


class ApiVersion(_ApiVersion, TypedDict, total=False):
    wsPath: str


class ServerApi(TypedDict):
    versions: Sequence[ApiVersion]


class ServerVersions(TypedDict):
    version: int
    serverVersion: str
    apis: Mapping[str, ServerApi]
