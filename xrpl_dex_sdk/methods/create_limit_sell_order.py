from ..models.common import MarketSymbol, BigNumberish
from ..models.ccxt.orders import OrderSide, OrderType
from ..models.methods.create_limit_sell_order import (
    CreateLimitSellOrderParams,
    CreateLimitSellOrderResponse,
)


def create_limit_sell_order(
    self,
    symbol: MarketSymbol,
    amount: BigNumberish,
    price: BigNumberish,
    params: CreateLimitSellOrderParams = CreateLimitSellOrderParams(),
) -> CreateLimitSellOrderResponse:
    order = self.create_order(
        symbol=symbol,
        side=OrderSide.Sell,
        type=OrderType.Limit,
        amount=amount,
        price=price,
        params=params,
    )

    return CreateLimitSellOrderResponse(id=order.id, info=order.info)
