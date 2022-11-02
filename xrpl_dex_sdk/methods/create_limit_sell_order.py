from ..models.common import MarketSymbol, BigNumberish
from ..models.ccxt.order import OrderSide, OrderType
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
    """
    Places a Limit Sell Order on the Ripple dEX.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        Market symbol for new Order
    amount : float
        How much currency you want to trade (in units of base currency)
    price : float
        Price at which the order is to be fullfilled (in units of quote currency)
    params : xrpl_dex_sdk.models.CreateLimitSellOrderParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.CreateLimitSellOrderResponse
        ID of created Order
    """

    order = self.create_order(
        symbol=symbol,
        side=OrderSide.Sell,
        type=OrderType.Limit,
        amount=amount,
        price=price,
        params=params,
    )

    return CreateLimitSellOrderResponse(id=order.id, info=order.info)
