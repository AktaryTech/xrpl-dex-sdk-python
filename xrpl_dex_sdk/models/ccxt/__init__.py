from ..common import AccountAddress

"""Top-level exports for the models.ccxt package."""
from .balances import Balance, Balances
from .fees import Fee
from .orders import Order, OrderId, OrderSide, OrderStatus, OrderTimeInForce, OrderType
from .trades import Trade, TradeId, TradeSide, TradeTakerOrMaker, TradeType


class OrderId:
    def __init__(self, account: AccountAddress, sequence: int) -> None:
        self.account = account
        self.sequence = sequence
        self.id = account + ":" + str(sequence)

    def __repr__(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.id


class TradeId:
    def __init__(self, account: AccountAddress, sequence: int) -> None:
        self.account = account
        self.sequence = sequence
        self.id = account + ":" + str(sequence)

    def __repr__(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.id


__all__ = [
    "Balance",
    "Balances",
    "Fee",
    "Order",
    "OrderId",
    "OrderSide",
    "OrderStatus",
    "OrderTimeInForce",
    "OrderType",
    "Trade",
    "TradeId",
    "TradeSide",
    "TradeTakerOrMaker",
    "TradeType",
]
