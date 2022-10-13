from typing import Optional

from ..constants import DEFAULT_LIMIT
from ..models import (
    FetchOrdersParams,
    FetchClosedOrdersParams,
    FetchClosedOrdersResponse,
    MarketSymbol,
    UnixTimestamp,
)


async def fetch_closed_orders(
    self,
    symbol: Optional[MarketSymbol] = None,
    since: Optional[UnixTimestamp] = None,
    limit: Optional[int] = DEFAULT_LIMIT,
    params: FetchClosedOrdersParams = FetchClosedOrdersParams(),
) -> FetchClosedOrdersResponse:
    orders = await self.fetch_orders(
        symbol,
        since,
        limit,
        FetchOrdersParams(search_limit=params.search_limit, show_open=False, show_canceled=False),
    )

    return orders
