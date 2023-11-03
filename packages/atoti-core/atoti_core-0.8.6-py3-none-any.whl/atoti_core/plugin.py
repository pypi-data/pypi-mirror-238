from collections.abc import Mapping
from pathlib import Path
from typing import Optional, Union

from .base_session import BaseSessionBound
from .empty_mapping import EMPTY_MAPPING


class Plugin:
    @property
    def app_extensions(self) -> Mapping[str, Union[str, Path]]:
        """The app extensions contributed by the plugin to be added to the session configuration."""
        return EMPTY_MAPPING

    @property
    def jar_path(self) -> Optional[Path]:
        """The path to the plugin's JAR.

        When not ``None``, the JAR will be added to the classpath of the Java process.
        """
        return None

    @property
    def java_package_name(self) -> Optional[str]:
        """The fully qualified name of the plugin's Java package.

        When not ``None``, the `init()` method of its class named like this Python class will be called before starting the application.
        """
        return None

    def post_init_session(self, session: BaseSessionBound, /) -> None:
        """Hook called at the end of *session*'s initialization."""
        ...
