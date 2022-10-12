from typing import List

from ..models import (
    FetchTickerParams,
    FetchTickerResponse,
    MarketSymbol,
    Ticker,
)


def fetch_tickers(
    self,
    symbols: List[MarketSymbol],
    params: FetchTickerParams = FetchTickerParams(),
) -> FetchTickerResponse:
    tickers: List[Ticker] = []

    for symbol in symbols:
        ticker = self.fetch_ticker(symbol, params)
        if ticker != None:
            tickers.append(ticker)

    return tickers
