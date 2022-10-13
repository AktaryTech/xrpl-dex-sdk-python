from typing import Callable, NamedTuple, Optional

from ...constants import DEFAULT_SEARCH_LIMIT


class WatchTickersParams(NamedTuple):
    # Listener to send balance updates to
    listener: Callable
    # Max Transactions to search through looking for Ticker data before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


__all__ = ["WatchTickersParams"]
