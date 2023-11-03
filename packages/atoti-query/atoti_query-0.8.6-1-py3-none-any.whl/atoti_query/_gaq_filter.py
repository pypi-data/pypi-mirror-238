from __future__ import annotations

from typing import Literal, Optional, Union

from atoti_core import Condition, Constant, HierarchyIdentifier, LevelIdentifier

GaqFilter = Condition[
    Union[HierarchyIdentifier, LevelIdentifier],
    Literal["eq", "isin"],
    Constant,
    Optional[Literal["and"]],
]
