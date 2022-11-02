from typing import Optional

from ..constants import DEFAULT_LIMIT
from ..models import (
    FetchOrdersParams,
    FetchOpenOrdersParams,
    FetchOpenOrdersResponse,
    MarketSymbol,
    UnixTimestamp,
)


async def fetch_open_orders(
    self,
    symbol: Optional[MarketSymbol] = None,
    since: Optional[UnixTimestamp] = None,
    limit: Optional[int] = DEFAULT_LIMIT,
    params: FetchOpenOrdersParams = FetchOpenOrdersParams(),
) -> FetchOpenOrdersResponse:
    """
    Fetches a list of open Orders from the dEX.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        (Optional) Market symbol to filter Orders by
    since : int
        (Optional) Only return Orders since this date
    limit : int
        (Optional) Total number of Orders to return (default is 20)
    params : xrpl_dex_sdk.models.FetchOpenOrdersParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchOpenOrdersResponse
        List of retrieved Orders
    """

    orders = await self.fetch_orders(
        symbol,
        since,
        limit,
        FetchOrdersParams(search_limit=params.search_limit, show_closed=False, show_canceled=False),
    )

    return orders
