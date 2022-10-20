from typing import List

from ..models import (
    FetchTickerParams,
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
        ticker = await self.fetch_ticker(symbol, FetchTickerParams.from_dict(params.to_dict()))
        if ticker != None:
            tickers.append(ticker)

    return tickers
