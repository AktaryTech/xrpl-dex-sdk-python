from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from ..common import MarketSymbol, UnixISOTimestamp, UnixTimestamp
from ..base_model import BaseModel
from ..required import REQUIRED


OrderBookEntry = List[float]


class OrderBookLevel(Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


@dataclass(frozen=True)
class OrderBook(BaseModel):
    """https://docs.ccxt.com/en/latest/manual.html?#order-book-structure"""

    symbol: MarketSymbol = REQUIRED
    nonce: Optional[int] = 0
    bids: List[OrderBookEntry] = REQUIRED
    asks: List[OrderBookEntry] = REQUIRED
    level: Optional[OrderBookLevel] = OrderBookLevel.L2
    timestamp: Optional[UnixTimestamp] = None
    datetime: Optional[UnixISOTimestamp] = None


OrderBooks = Dict[MarketSymbol, OrderBook]
