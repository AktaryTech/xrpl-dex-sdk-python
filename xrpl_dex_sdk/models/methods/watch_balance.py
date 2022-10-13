from typing import Callable, NamedTuple, Optional

from ..common import CurrencyCode


class WatchBalanceParams(NamedTuple):
    # Listener to send balance updates to
    listener: Callable
    # Currency to fetch balances for
    code: Optional[CurrencyCode] = None


__all__ = ["WatchBalanceParams"]
