from typing import NamedTuple, Optional

from ...models.ccxt import Trades
from ...constants import DEFAULT_SEARCH_LIMIT


class FetchMyTradesParams(NamedTuple):
    # Max items to search through looking for Trades before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


FetchMyTradesResponse = Trades

__all__ = ["FetchMyTradesParams", "FetchMyTradesResponse"]
