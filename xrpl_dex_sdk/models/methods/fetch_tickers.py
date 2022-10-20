from typing import List, NamedTuple, Optional

from ...models.ccxt import Ticker
from ...constants import DEFAULT_SEARCH_LIMIT


class FetchTickersParams(NamedTuple):
    # Max Transactions to search through looking for Tickers data before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


FetchTickersResponse = List[Ticker]

__all__ = ["FetchTickersParams", "FetchTickersResponse"]
