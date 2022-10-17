from typing import NamedTuple, Optional, Union

from ...constants import DEFAULT_SEARCH_LIMIT
from ...models.ccxt import Order


class FetchOrderParams(NamedTuple):
    # Max items to search through looking for an Order before giving up
    search_limit: int = DEFAULT_SEARCH_LIMIT
    # Ledger index containing the Order (optional)
    ledger_index: Optional[Union[int, str]] = None


FetchOrderResponse = Order

__all__ = ["FetchOrderParams", "FetchOrderResponse"]
