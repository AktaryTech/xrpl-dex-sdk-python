from ..models.common import MarketSymbol
from ..models.ccxt.orders import OrderSide, OrderType
from ..models.methods.create_limit_buy_order import (
    CreateLimitBuyOrderParams,
    CreateLimitBuyOrderResponse,
)


def create_limit_buy_order(
    self,
    symbol: MarketSymbol,
    amount: str,
    price: str,
    params: CreateLimitBuyOrderParams = CreateLimitBuyOrderParams(),
) -> CreateLimitBuyOrderResponse:
    return self.create_order(
        symbol=symbol,
        side=OrderSide.Buy,
        type=OrderType.Limit,
        amount=amount,
        price=price,
        params=params,
    )
