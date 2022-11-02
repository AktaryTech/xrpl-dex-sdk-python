from ..models.common import MarketSymbol, BigNumberish
from ..models.ccxt.order import OrderSide, OrderType
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
    """
    Places a Limit Buy Order on the Ripple dEX.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        Market symbol for new Order
    amount : float
        How much currency you want to trade (in units of base currency)
    price : float
        Price at which the order is to be fullfilled (in units of quote currency)
    params : xrpl_dex_sdk.models.CreateLimitBuyOrderParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.CreateLimitBuyOrderResponse
        ID of created Order
    """

    order = self.create_order(
        symbol=symbol,
        side=OrderSide.Buy,
        type=OrderType.Limit,
        amount=amount,
        price=price,
        params=params,
    )

    return CreateLimitBuyOrderResponse(id=order.id, info=order.info)
