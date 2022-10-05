from typing import Any, Dict, NamedTuple, Optional

from ...models import AccountAddress, CurrencyCode
from ...models.ccxt.orders import Order


class FetchOrderParams(NamedTuple):
    # Max items to search through looking for an Order before giving up
    search_limit: int
    # Ledger index containing the Order (optional)
    ledger_index: Optional[int or str]


FetchOrderResponse = Order or None
