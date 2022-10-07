from typing import List, NamedTuple, Optional

from ...models.ccxt import Order
from ...constants import DEFAULT_SEARCH_LIMIT


class FetchOrdersParams(NamedTuple):
    # Max Transactions to search through looking for Order data before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT
    # Whether to return Open orders
    show_open: Optional[bool] = True
    # Whether to return Closed orders
    show_closed: Optional[bool] = True
    # Whether to return Canceled orders
    show_canceled: Optional[bool] = True


FetchOrdersResponse = List[Order]

__all__ = ["FetchOrdersParams", "FetchOrdersResponse"]
