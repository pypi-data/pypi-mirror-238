from collections.abc import Mapping
from dataclasses import dataclass
from functools import cached_property

from atoti_core import keyword_only_dataclass
from typing_extensions import override

from .auth import Auth


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class TokenAuthentication(Auth):
    """Also called "Bearer authentication", this :class:`atoti_query.Auth`, passes the given token to the HTTP :guilabel:`Authorization` header of the request being made."""

    token: str
    token_type: str = "Bearer"

    @override
    def __call__(
        self,
        url: str,
    ) -> Mapping[str, str]:
        return self._headers

    @cached_property
    def _headers(self) -> Mapping[str, str]:
        return {"Authorization": f"{self.token_type} {self.token}"}
