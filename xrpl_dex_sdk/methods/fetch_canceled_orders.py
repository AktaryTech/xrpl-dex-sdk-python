from typing import Optional

from ..constants import DEFAULT_LIMIT
from ..models import (
    FetchOrdersParams,
    FetchCanceledOrdersParams,
    FetchCanceledOrdersResponse,
    MarketSymbol,
    UnixTimestamp,
)


async def fetch_canceled_orders(
    self,
    symbol: Optional[MarketSymbol] = None,
    since: Optional[UnixTimestamp] = None,
    limit: Optional[int] = DEFAULT_LIMIT,
    params: FetchCanceledOrdersParams = FetchCanceledOrdersParams(),
) -> FetchCanceledOrdersResponse:
    orders = await self.fetch_orders(
        symbol,
        since,
        limit,
        FetchOrdersParams(search_limit=params.search_limit, show_open=False, show_closed=False),
    )

    return orders
