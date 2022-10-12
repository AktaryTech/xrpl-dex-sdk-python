from typing import NamedTuple, Optional

from ...models.ccxt import Ticker
from ...constants import DEFAULT_SEARCH_LIMIT


class FetchTickerParams(NamedTuple):
    # Max Transactions to search through looking for Ticker data before giving up
    search_limit: int = DEFAULT_SEARCH_LIMIT


FetchTickerResponse = Ticker

__all__ = ["FetchTickerParams", "FetchTickerResponse"]
