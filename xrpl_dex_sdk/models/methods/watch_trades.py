from typing import Callable, NamedTuple, Optional

from ...constants import DEFAULT_SEARCH_LIMIT


class WatchTradesParams(NamedTuple):
    # Listener to send balance updates to
    listener: Callable
    # Max items to search through looking for Trades before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


__all__ = ["WatchTradesParams"]
