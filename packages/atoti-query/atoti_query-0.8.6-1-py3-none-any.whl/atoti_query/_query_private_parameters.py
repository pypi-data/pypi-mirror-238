from dataclasses import dataclass
from typing import Optional

from atoti_core import keyword_only_dataclass

from ._get_data_types import GetDataTypes


@keyword_only_dataclass
@dataclass(frozen=True)
class QueryPrivateParameters:
    get_data_types: Optional[GetDataTypes] = None
