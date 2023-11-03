from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from atoti_core import Constant, keyword_only_dataclass

_MemberPath = tuple[Constant, ...]


@keyword_only_dataclass
@dataclass(frozen=True)
class HierarchyFilter:
    member_paths: Sequence[_MemberPath]
    exclusion: bool = False

    def __and__(self, other: HierarchyFilter, /) -> HierarchyFilter:
        if not (self.exclusion and other.exclusion):
            raise ValueError("Only exclusion filters can be combined.")

        return HierarchyFilter(
            exclusion=True,
            member_paths=[*self.member_paths, *other.member_paths],
        )
