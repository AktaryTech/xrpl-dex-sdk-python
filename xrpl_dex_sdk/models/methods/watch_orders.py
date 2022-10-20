from typing import Callable, NamedTuple, Optional

from ...constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT


class WatchOrdersParams(NamedTuple):
    # Listener to send balance updates to
    listener: Callable
    # Number of results to return
    limit: Optional[int] = DEFAULT_LIMIT
    # Max Transactions to search through looking for Order data before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT
    # Whether to return Open orders
    show_open: Optional[bool] = True
    # Whether to return Closed orders
    show_closed: Optional[bool] = True
    # Whether to return Canceled orders
    show_canceled: Optional[bool] = True


__all__ = ["WatchOrdersParams"]
