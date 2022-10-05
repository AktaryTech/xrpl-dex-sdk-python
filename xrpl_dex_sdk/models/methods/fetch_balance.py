from typing import NamedTuple, Optional

from ...models import AccountAddress, CurrencyCode
from ...models.ccxt.balances import Balances


class FetchBalanceParams(NamedTuple):
    account: AccountAddress
    code: Optional[CurrencyCode]


FetchBalanceResponse = Balances or None
