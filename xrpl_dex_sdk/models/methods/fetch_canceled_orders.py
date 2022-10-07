from typing import List, NamedTuple, Optional

from ...models.ccxt import Order
from ...constants import DEFAULT_SEARCH_LIMIT


class FetchCanceledOrdersParams(NamedTuple):
    # Max Transactions to search through looking for Order data before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


FetchCanceledOrdersResponse = List[Order]
