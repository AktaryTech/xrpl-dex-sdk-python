from dataclasses import dataclass
from typing import Optional, Union

from ...constants import DEFAULT_SEARCH_LIMIT
from ...models.ccxt import Order
from ..base_model import BaseModel


@dataclass(frozen=True)
class FetchOrderParams(BaseModel):
    # Max items to search through looking for an Order before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT
    # Ledger index containing the Order (optional)
    ledger_index: Optional[Union[int, str]] = None


FetchOrderResponse = Order
