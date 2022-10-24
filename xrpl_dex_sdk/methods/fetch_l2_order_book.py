from ..constants import DEFAULT_LIMIT
from ..models import (
    FetchL2OrderBookParams,
    FetchL2OrderBookResponse,
    MarketSymbol,
)


async def fetch_l2_order_book(
    self,
    symbol: MarketSymbol,
    limit: int = DEFAULT_LIMIT,
    params: FetchL2OrderBookParams = FetchL2OrderBookParams(),
) -> FetchL2OrderBookResponse:
    """
    Retrieves L2 order book data for a single market pair.

    Parameters
    ----------
    symbol : MarketSymbol
        Market symbol to get order book for
    limit : int
        (Optional) Total number of entries to return (default is 20)
    params : FetchL2OrderBookParams
        (Optional) Additional request parameters

    Returns
    -------
    FetchL2OrderBookResponse
        Order book
    """

    return await self.fetch_order_book(symbol=symbol, limit=limit, params=params)
