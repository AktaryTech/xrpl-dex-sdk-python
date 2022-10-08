from enum import Enum
from typing import List, NamedTuple, Optional

from ..common import MarketSymbol, UnixISOTimestamp, UnixTimestamp


class OrderBookEntryType(Enum):
    BID: str = "bid"
    ASK: str = "ask"


class OrderBookEntry(NamedTuple):
    type: OrderBookEntryType
    price: float
    amount: float


class OrderBookLevel(Enum):
    L1: str = "L1"
    L2: str = "L2"
    L3: str = "L3"


class OrderBook(NamedTuple):
    symbol: MarketSymbol
    nonce: int
    bids: List[OrderBookEntry] = []
    asks: List[OrderBookEntry] = []
    timestamp: Optional[UnixTimestamp] = None
    datetime: Optional[UnixISOTimestamp] = None


__all__ = [
    "OrderBookEntryType",
    "OrderBookEntry",
    "OrderBookLevel",
    "OrderBook",
]
