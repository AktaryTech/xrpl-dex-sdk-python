from dataclasses import dataclass
from typing import List, Optional

from ...models.ccxt import Order
from ...constants import DEFAULT_SEARCH_LIMIT
from ..base_model import BaseModel


@dataclass(frozen=True)
class FetchOpenOrdersParams(BaseModel):
    # Max Transactions to search through looking for Order data before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


FetchOpenOrdersResponse = List[Order]
