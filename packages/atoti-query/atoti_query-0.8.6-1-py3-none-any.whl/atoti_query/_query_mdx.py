from datetime import timedelta
from typing import Any, Literal, Protocol

import pandas as pd
from atoti_core import DEFAULT_QUERY_TIMEOUT, EMPTY_MAPPING, Context


class QueryMdx(Protocol):
    def __call__(
        self,
        mdx: str,
        *,
        context: Context = EMPTY_MAPPING,
        keep_totals: bool = False,
        mode: Literal["pretty", "raw"] = "pretty",
        timeout: timedelta = DEFAULT_QUERY_TIMEOUT,
        **kwargs: Any,
    ) -> pd.DataFrame:
        ...
