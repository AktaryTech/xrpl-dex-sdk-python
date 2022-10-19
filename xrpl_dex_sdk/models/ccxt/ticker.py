from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from ..common import MarketSymbol, UnixISOTimestamp, UnixTimestamp
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class Ticker(BaseModel):
    # symbol of the market ('BTC/USD', 'ETH/BTC', ...)
    symbol: MarketSymbol = REQUIRED
    # (64-bit Unix Timestamp in milliseconds since Epoch 1 Jan 1970)
    timestamp: UnixTimestamp = REQUIRED
    # ISO8601 datetime str with milliseconds
    datetime: UnixISOTimestamp = REQUIRED
    # highest price
    high: float = REQUIRED
    # lowest price
    low: float = REQUIRED
    # current best bid (buy) price
    bid: float = REQUIRED
    # current best bid (buy) amount (may be missing or undefined)
    bid_volume: Optional[float] = None
    # current best ask (sell) price
    ask: float = REQUIRED
    # current best ask (sell) amount (may be missing or undefined)
    ask_volume: Optional[float] = None
    # volume weighed average price
    vwap: float = REQUIRED
    # opening price
    open: float = REQUIRED
    # price of last trade (closing price for current period)
    close: float = REQUIRED
    # same as `close`, duplicated for convenience
    last: float = REQUIRED
    # closing price for the previous period
    previous_close: float = REQUIRED
    # absolute change, `last - open`
    change: float = REQUIRED
    # relative change, `(change/open) * 100`
    percentage: float = REQUIRED
    # average price, `(last + open) / 2`
    average: float = REQUIRED
    # volume of base currency traded for last 24 hours
    base_volume: float = REQUIRED
    # volume of quote currency traded for last 24 hours
    quote_volume: float = REQUIRED
    # the original non-modified unparsed reply from exchange API
    info: Dict[str, Any] = REQUIRED


Tickers = Dict[MarketSymbol, Ticker]


__all__ = ["Ticker", "Tickers"]
