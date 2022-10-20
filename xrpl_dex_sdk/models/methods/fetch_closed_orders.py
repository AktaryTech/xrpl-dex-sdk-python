from dataclasses import dataclass
from typing import List, Optional

from ..base_model import BaseModel
from ..ccxt import Order
from ...constants import DEFAULT_SEARCH_LIMIT


@dataclass(frozen=True)
class FetchClosedOrdersParams(BaseModel):
    # Max Transactions to search through looking for Order data before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


FetchClosedOrdersResponse = List[Order]

__all__ = ["FetchClosedOrdersParams", "FetchClosedOrdersResponse"]
