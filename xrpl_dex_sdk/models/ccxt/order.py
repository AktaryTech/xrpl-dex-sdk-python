from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from ..common import OrderId, MarketSymbol, UnixISOTimestamp, UnixTimestamp
from .fees import Fee
from .trades import Trade
from ..base_model import BaseModel
from ..required import REQUIRED


class OrderStatus(Enum):
    Open = "open"
    Closed = "closed"
    Canceled = "canceled"
    Expired = "expired"
    Rejected = "rejected"


class OrderType(Enum):
    Limit = "limit"


class OrderTimeInForce(Enum):
    GoodTillCanceled = "GTC"
    ImmediateOrCancel = "IOC"
    FillOrKill = "FOK"
    PostOnly = "PO"


class OrderSide(Enum):
    Buy = "buy"
    Sell = "sell"


@dataclass(frozen=True)
class Order(BaseModel):
    """https://docs.ccxt.com/en/latest/manual.html?#order-structure"""

    id: OrderId = REQUIRED
    client_order_id: Optional[str] = None
    datetime: UnixISOTimestamp = REQUIRED
    timestamp: UnixTimestamp = REQUIRED
    last_trade_timestamp: Optional[UnixTimestamp] = None
    status: OrderStatus = REQUIRED
    symbol: MarketSymbol = REQUIRED
    type: OrderType = REQUIRED
    time_in_force: Optional[OrderTimeInForce] = None
    side: OrderSide = REQUIRED
    amount: float = REQUIRED
    price: float = REQUIRED
    average: Optional[float] = None
    filled: float = REQUIRED
    remaining: float = REQUIRED
    cost: float = REQUIRED
    trades: List[Trade] = REQUIRED
    fee: Optional[Fee] = None
    info: dict = REQUIRED
