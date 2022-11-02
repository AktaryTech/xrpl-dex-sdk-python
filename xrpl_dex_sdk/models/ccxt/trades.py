from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from .fees import Fee
from ..common import (
    MarketSymbol,
    UnixISOTimestamp,
    UnixTimestamp,
    OrderId,
    TradeId,
)
from ..base_model import BaseModel
from ..required import REQUIRED


class TradeType(Enum):
    Limit = "limit"


class TradeSide(Enum):
    Buy = "buy"
    Sell = "sell"


class TradeTakerOrMaker(Enum):
    Taker = "taker"
    Maker = "maker"


@dataclass(frozen=True)
class Trade(BaseModel):
    """https://docs.ccxt.com/en/latest/manual.html?#trade-structure"""

    # string trade id
    id: TradeId = REQUIRED
    # string order id or undefined/None/null
    order: OrderId = REQUIRED
    # ISO8601 datetime with milliseconds;
    datetime: UnixISOTimestamp = REQUIRED
    # Unix timestamp in milliseconds
    timestamp: UnixTimestamp = REQUIRED
    # symbol in CCXT format
    symbol: MarketSymbol = REQUIRED
    # order type, 'market', 'limit', ... or undefined/None/null
    type: Optional[TradeType] = TradeType.Limit
    # direction of the trade, 'buy' or 'sell'
    side: TradeSide = REQUIRED
    # amount of base currency
    amount: float = REQUIRED
    # float price in quote currency
    price: float = REQUIRED
    # | 'maker'; string, 'taker' or 'maker'
    taker_or_maker: TradeTakerOrMaker = REQUIRED
    # total cost (including fees), `price * amount`
    cost: float = REQUIRED
    # transfer fees
    fee: Optional[Fee] = None
    # Raw response from exchange
    info: dict = REQUIRED


Trades = List[Trade]
