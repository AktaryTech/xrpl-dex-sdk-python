from typing import NamedTuple, Optional

from ...models.ccxt import Balances
from ..common import CurrencyCode


class FetchBalanceParams(NamedTuple):
    code: Optional[CurrencyCode]


FetchBalanceResponse = Balances or None
