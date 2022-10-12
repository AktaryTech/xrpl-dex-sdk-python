from ..constants import DEFAULT_LIMIT
from ..models import (
    FetchL2OrderBookParams,
    FetchL2OrderBookResponse,
    MarketSymbol,
)


def fetch_l2_order_book(
    self,
    symbol: MarketSymbol,
    limit: int = DEFAULT_LIMIT,
    params: FetchL2OrderBookParams = FetchL2OrderBookParams(),
) -> FetchL2OrderBookResponse:
    return self.fetch_order_book(symbol=symbol, limit=limit, params=params)
