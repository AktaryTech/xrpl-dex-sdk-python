from ..models.common import MarketSymbol
from ..models.ccxt.orders import OrderSide, OrderType
from ..models.methods.create_limit_sell_order import (
    CreateLimitSellOrderParams,
    CreateLimitSellOrderResponse,
)


def create_limit_sell_order(
    self,
    symbol: MarketSymbol,
    amount: str,
    price: str,
    params: CreateLimitSellOrderParams = CreateLimitSellOrderParams(),
) -> CreateLimitSellOrderResponse:
    return self.create_order(
        symbol=symbol,
        side=OrderSide.Sell,
        type=OrderType.Limit,
        amount=amount,
        price=price,
        params=params,
    )
