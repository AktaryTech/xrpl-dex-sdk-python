from typing import Optional

from ..constants import DEFAULT_LIMIT
from ..models import (
    FetchOrdersParams,
    FetchOpenOrdersParams,
    FetchOpenOrdersResponse,
    MarketSymbol,
    UnixTimestamp,
)


def fetch_open_orders(
    self,
    symbol: Optional[MarketSymbol] = None,
    since: Optional[UnixTimestamp] = None,
    limit: Optional[int] = DEFAULT_LIMIT,
    params: FetchOpenOrdersParams = FetchOpenOrdersParams(),
) -> FetchOpenOrdersResponse:
    orders = self.fetch_orders(
        symbol,
        since,
        limit,
        FetchOrdersParams(search_limit=params.search_limit, show_closed=False, show_canceled=False),
    )

    return orders
