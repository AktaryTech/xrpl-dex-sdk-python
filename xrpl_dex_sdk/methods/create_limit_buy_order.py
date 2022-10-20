from ..models.common import MarketSymbol, BigNumberish
from ..models.ccxt.orders import OrderSide, OrderType
from ..models.methods.create_limit_buy_order import (
    CreateLimitBuyOrderParams,
    CreateLimitBuyOrderResponse,
)


def create_limit_buy_order(
    self,
    symbol: MarketSymbol,
    amount: BigNumberish,
    price: BigNumberish,
    params: CreateLimitBuyOrderParams = CreateLimitBuyOrderParams(),
) -> CreateLimitBuyOrderResponse:
    order = self.create_order(
        symbol=symbol,
        side=OrderSide.Buy,
        type=OrderType.Limit,
        amount=amount,
        price=price,
        params=params,
    )

    return CreateLimitBuyOrderResponse(id=order.id, info=order.info)
