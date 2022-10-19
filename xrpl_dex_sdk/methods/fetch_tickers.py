from typing import List

from ..models import (
    FetchTickersParams,
    FetchTickersResponse,
    MarketSymbol,
    Ticker,
)


async def fetch_tickers(
    self, symbols: List[MarketSymbol], params: FetchTickersParams = FetchTickersParams()
) -> FetchTickersResponse:
    tickers: List[Ticker] = []

    for symbol in symbols:
        ticker = await self.fetch_ticker(symbol, params)
        if ticker != None:
            tickers.append(ticker)

    return tickers
