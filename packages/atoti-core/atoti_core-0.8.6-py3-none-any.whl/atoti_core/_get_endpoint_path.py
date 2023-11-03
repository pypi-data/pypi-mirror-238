from collections.abc import Collection
from typing import Literal

from ._server_versions import ServerVersions

_SUPPORTED_PIVOT_VERSIONS = ("4", "5", "6", "7zz1", "8zz1", "8zz2", "8")


def _get_supported_version_index(
    server_versions: ServerVersions,
    *,
    namespace: str,
    supported_versions: Collection[str],
) -> int:
    exposed_versions = [
        version["id"] for version in server_versions["apis"][namespace]["versions"]
    ]

    try:
        return next(
            index
            for index, version in enumerate(exposed_versions)
            if version in supported_versions
        )
    except StopIteration as error:
        raise RuntimeError(
            f"Exposed {namespace} versions: {exposed_versions} do not match the supported ones: {supported_versions}."
        ) from error


def get_endpoint_path(
    *,
    attribute_name: Literal["restPath", "wsPath"] = "restPath",
    namespace: str,
    route: str,
    server_versions: ServerVersions,
) -> str:
    assert not route.startswith("/")
    assert (
        "?" not in route
    ), f"Expected the route to not contain a query string, but got `{route}`."

    version_index = (
        _get_supported_version_index(
            server_versions,
            namespace=namespace,
            supported_versions=_SUPPORTED_PIVOT_VERSIONS,
        )
        if namespace in {"activeviam/pivot", "pivot"}
        else 0
    )

    path = server_versions["apis"][namespace]["versions"][version_index].get(
        attribute_name
    )

    if path is None:
        raise RuntimeError(f"Missing `{attribute_name}` for `{namespace}` namespace.")

    return f"{path.lstrip('/')}/{route}"
