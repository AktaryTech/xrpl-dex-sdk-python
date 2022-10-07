from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional

from ..common import MarketSymbol, UnixISOTimestamp, UnixTimestamp


class Ticker(NamedTuple):
    # symbol of the market ('BTC/USD', 'ETH/BTC', ...)
    symbol: MarketSymbol
    # (64-bit Unix Timestamp in milliseconds since Epoch 1 Jan 1970)
    timestamp: UnixTimestamp
    # ISO8601 datetime str with milliseconds
    datetime: UnixISOTimestamp
    # highest price
    high: float
    # lowest price
    low: float
    # current best bid (buy) price
    bid: float
    # current best bid (buy) amount (may be missing or undefined)
    bid_volume: Optional[float]
    # current best ask (sell) price
    ask: float
    # current best ask (sell) amount (may be missing or undefined)
    ask_volume: Optional[float]
    # volume weighed average price
    vwap: float
    # opening price
    open: float
    # price of last trade (closing price for current period)
    close: float
    # same as `close`, duplicated for convenience
    last: float
    # closing price for the previous period
    previous_close: float
    # absolute change, `last - open`
    change: float
    # relative change, `(change/open) * 100`
    percentage: float
    # average price, `(last + open) / 2`
    average: float
    # volume of base currency traded for last 24 hours
    base_volume: float
    # volume of quote currency traded for last 24 hours
    quote_volume: float
    # the original non-modified unparsed reply from exchange API
    info: Dict[str, Any]


__all__ = [
    "Ticker",
]
