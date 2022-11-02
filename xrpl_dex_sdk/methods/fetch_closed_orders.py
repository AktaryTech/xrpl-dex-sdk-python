from typing import Optional

from ..constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT
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
    """
    Fetches a list of closed Orders from the dEX.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        (Optional) Market symbol to filter Orders by
    since : int
        (Optional) Only return Orders since this date
    limit : int
        (Optional) Total number of Orders to return (default is 20)
    params : xrpl_dex_sdk.models.FetchClosedOrdersParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchClosedOrdersResponse
        List of retrieved Orders
    """

    orders = await self.fetch_orders(
        symbol,
        since,
        limit,
        FetchOrdersParams(
            search_limit=params.search_limit
            if params.search_limit != None
            else DEFAULT_SEARCH_LIMIT,
            show_open=False,
            show_canceled=False,
        ),
    )

    return orders
