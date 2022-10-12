from typing import NamedTuple, Optional

from ...models.ccxt import Balances
from ..common import CurrencyCode


class WatchBalanceParams(NamedTuple):
    code: Optional[CurrencyCode]


WatchBalanceResponse = Balances or None

__all__ = ["WatchBalanceParams", "WatchBalanceResponse"]
