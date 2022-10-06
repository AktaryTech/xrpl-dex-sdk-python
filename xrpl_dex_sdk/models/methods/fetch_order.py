from typing import NamedTuple, Optional

from ...models.ccxt import Order


class FetchOrderParams(NamedTuple):
    # Max items to search through looking for an Order before giving up
    search_limit: int
    # Ledger index containing the Order (optional)
    ledger_index: Optional[int or str]


FetchOrderResponse = Order or None
