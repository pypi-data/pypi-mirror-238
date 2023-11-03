from typing import Union

from .has_identifier import HasIdentifier, IdentifierT_co


def identify(
    identifiable: Union[HasIdentifier[IdentifierT_co], IdentifierT_co], /
) -> IdentifierT_co:
    return (
        identifiable._identifier
        if isinstance(identifiable, HasIdentifier)
        else identifiable
    )
