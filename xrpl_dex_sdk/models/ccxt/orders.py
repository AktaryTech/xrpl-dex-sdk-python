from enum import Enum


class OrderStatus(Enum):
    Open: str = "open"
    Closed: str = "closed"
    Canceled: str = "canceled"
    Expired: str = "expired"
    Rejected: str = "rejected"


class OrderType(Enum):
    Limit: str = "limit"
    Market: str = "market"


class OrderTimeInForce(Enum):
    GoodTillCanceled: str = "gtc"
    ImmediateOrCancel: str = "ioc"
    FillOrKill: str = "fok"
    PostOnly: str = "po"


class OrderSide(Enum):
    Buy: str = "buy"
    Sell: str = "sell"
