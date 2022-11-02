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
    """
    Retrieves price ticker data for a multiple market pairs.

    Parameters
    ----------
    symbols : List[xrpl_dex_sdk.models.MarketSymbol]
        List of market symbols to get price ticker data for
    params : xrpl_dex_sdk.models.FetchTickersParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchTickersResponse
        Price ticker data
    """

    tickers: List[Ticker] = []

    for symbol in symbols:
        ticker = await self.fetch_ticker(symbol, FetchTickerParams.from_dict(params.to_dict()))
        if ticker != None:
            tickers.append(ticker)

    return tickers
