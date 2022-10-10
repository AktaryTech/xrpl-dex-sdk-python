from enum import Enum
from typing import Dict, List, NamedTuple, Optional

from ..common import MarketSymbol, UnixISOTimestamp, UnixTimestamp


OrderBookEntry = List[float]


class OrderBookLevel(Enum):
    L1: str = "L1"
    L2: str = "L2"
    L3: str = "L3"


class OrderBook(NamedTuple):
    symbol: MarketSymbol
    nonce: int
    bids: List[OrderBookEntry] = []
    asks: List[OrderBookEntry] = []
    level: Optional[OrderBookLevel] = OrderBookLevel.L2
    timestamp: Optional[UnixTimestamp] = None
    datetime: Optional[UnixISOTimestamp] = None


OrderBooks = Dict[MarketSymbol, OrderBook]


__all__ = [
    "OrderBookEntry",
    "OrderBookLevel",
    "OrderBook",
    "OrderBooks",
]
