from collections.abc import Iterable
from typing import Protocol

from atoti_core import DataType, IdentifierT_co


class GetDataTypes(Protocol):
    def __call__(
        self, identifier: Iterable[IdentifierT_co], /, *, cube_name: str
    ) -> dict[IdentifierT_co, DataType]:
        ...
