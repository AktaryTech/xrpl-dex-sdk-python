from typing import List, NamedTuple, Optional

from ...models.ccxt import Order


class FetchOrdersParams(NamedTuple):
    # Max Transactions to search through looking for Order data before giving up
    search_limit: int
    # Whether to return Open orders
    show_open: bool
    # Whether to return Closed orders
    show_closed: bool
    # Whether to return Canceled orders
    show_canceled: bool


FetchOrdersResponse = List[Order]
