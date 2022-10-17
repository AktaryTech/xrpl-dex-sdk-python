from typing import NamedTuple, Optional

from ...models.ccxt import Balances
from ..common import CurrencyCode


class FetchBalanceParams(NamedTuple):
    code: Optional[CurrencyCode] = None


FetchBalanceResponse = Balances or None

__all__ = ["FetchBalanceParams", "FetchBalanceResponse"]
