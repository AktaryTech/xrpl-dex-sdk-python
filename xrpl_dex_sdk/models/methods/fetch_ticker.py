from dataclasses import dataclass
from typing import Optional

from ...models.ccxt import Ticker
from ...constants import DEFAULT_TICKER_SEARCH_LIMIT
from ..base_model import BaseModel


@dataclass(frozen=True)
class FetchTickerParams(BaseModel):
    # Max Transactions to search through looking for Ticker data before giving up
    search_limit: Optional[int] = DEFAULT_TICKER_SEARCH_LIMIT


FetchTickerResponse = Ticker
