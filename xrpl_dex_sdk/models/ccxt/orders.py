from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional

from .. import AccountAddress, MarketSymbol, UnixISOTimestamp, UnixTimestamp
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
    Open: str = "open"
    Closed: str = "closed"
    Canceled: str = "canceled"
    Expired: str = "expired"
    Rejected: str = "rejected"


class OrderType(Enum):
    Limit: str = "limit"


class OrderTimeInForce(Enum):
    GoodTillCanceled: str = "GTC"
    ImmediateOrCancel: str = "IOC"
    FillOrKill: str = "FOK"
    PostOnly: str = "PO"


class OrderSide(Enum):
    Buy: str = "buy"
    Sell: str = "sell"


class Order(NamedTuple):
    id: OrderId
    clientOrderId: Optional[str]
    datetime: UnixISOTimestamp
    timestamp: UnixTimestamp
    lastTradeTimestamp: UnixTimestamp
    status: OrderStatus
    symbol: MarketSymbol
    type: OrderType
    timeInForce: Optional[OrderTimeInForce]
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
