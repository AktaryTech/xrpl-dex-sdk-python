from typing import Any, Dict, NamedTuple, Optional

from ...models import AccountAddress, CurrencyCode
from ...models.ccxt.balances import Balance


class FetchBalanceParams(NamedTuple):
    account: AccountAddress
    code: Optional[CurrencyCode]


class FetchBalanceResponse(NamedTuple):
    balances: Dict[CurrencyCode, Balance]
    info: Dict[str, Any]
