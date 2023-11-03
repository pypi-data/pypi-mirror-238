from typing import Union

from .has_identifier import HasIdentifier, IdentifierT_co

Identifiable = Union[HasIdentifier[IdentifierT_co], IdentifierT_co]
