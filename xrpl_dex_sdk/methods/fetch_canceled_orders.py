from typing import Optional

from ..constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT
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
    """
    Fetches a list of canceled Orders from the dEX.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        (Optional) Market symbol to filter Orders by
    since : int
        (Optional) Only return Orders since this date
    limit : int
        (Optional) Total number of Orders to return (default is 20)
    params : xrpl_dex_sdk.models.FetchCanceledOrdersParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchCanceledOrdersResponse
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
            show_closed=False,
        ),
    )

    return orders
