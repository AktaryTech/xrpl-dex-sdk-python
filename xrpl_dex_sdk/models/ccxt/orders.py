from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional

from ..common import AccountAddress, MarketSymbol, UnixISOTimestamp, UnixTimestamp
from .fees import Fee
from .trades import Trade


class OrderId:
    def __init__(self, account: AccountAddress, sequence: int) -> None:
        self.account = account
        self.sequence = sequence
        self.id = account + ":" + str(sequence)

    def __repr__(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.id


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


class Order(NamedTuple):
    id: OrderId
    client_order_id: Optional[str]
    datetime: UnixISOTimestamp
    timestamp: UnixTimestamp
    last_trade_timestamp: Optional[UnixTimestamp]
    status: OrderStatus
    symbol: MarketSymbol
    type: OrderType
    time_in_force: Optional[OrderTimeInForce]
    side: OrderSide
    amount: float
    price: float
    average: Optional[float]
    filled: float
    remaining: float
    cost: float
    trades: List[Trade]
    fee: Optional[Fee]
    info: Dict[str, Any]


__all__ = [
    "OrderId",
    "OrderStatus",
    "OrderType",
    "OrderTimeInForce",
    "OrderSide",
    "Order",
]
