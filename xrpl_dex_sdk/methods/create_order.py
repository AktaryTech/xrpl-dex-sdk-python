from xrpl.utils import xrp_to_drops
from xrpl.transaction import safe_sign_and_submit_transaction
from xrpl.models.transactions import OfferCreate
from xrpl.models.amounts import (
    Amount as XrplAmount,
    IssuedCurrencyAmount as XrplIssuedCurrencyAmount,
)

from ..models import (
    MarketSymbol,
    BigNumberish,
    OrderId,
    OrderSide,
    OrderType,
    CreateOrderParams,
    CreateOrderResponse,
    OfferCreateFlags,
)
from ..utils import handle_response_error, get_base_amount_key


def create_order(
    self,
    symbol: MarketSymbol,
    side: OrderSide,
    # unused - always "limit"
    type: OrderType,
    amount: BigNumberish,
    price: BigNumberish,
    params: CreateOrderParams = CreateOrderParams(),
) -> CreateOrderResponse:
    """
    Places an Order on the Ripple dEX.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        Market symbol for new Order
    side : xrpl_dex_sdk.models.OrderSide
        Order direction (buy or sell)
    type : xrpl_dex_sdk.models.OrderType
        Order type. Only limit orders are supported
    amount : float
        How much currency you want to trade (in units of base currency)
    price : float
        Price at which the order is to be fullfilled (in units of quote currency)
    params : xrpl_dex_sdk.models.CreateOrderParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.CreateOrderResponse
        ID of created Order
    """

    amount = float(amount)
    price = float(price)

    base_amount = (
        XrplIssuedCurrencyAmount(
            currency=symbol.base.currency,
            issuer=symbol.base.issuer,
            value=amount,
        )
        if symbol.base.issuer
        else xrp_to_drops(amount)
    )
    base_amount_key = get_base_amount_key(side)

    quote_amount = (
        XrplIssuedCurrencyAmount(
            currency=symbol.quote.currency,
            issuer=symbol.quote.issuer,
            value=amount * price,
        )
        if symbol.quote.issuer != None
        else xrp_to_drops(amount * price)
    )

    offer_create_request = {
        "account": self.wallet.classic_address,
        "flags": 0,
        "taker_gets": base_amount if base_amount_key == "TakerGets" else quote_amount,
        "taker_pays": base_amount if base_amount_key == "TakerPays" else quote_amount,
    }

    for field in params.__dataclass_fields__:
        if getattr(params, field) != None:
            offer_create_request[field] = params.__getattribute__(field)

    if params.flags != None:
        for flag in params.flags:
            flagEnum = getattr(OfferCreateFlags, flag)
            if flagEnum != None and flagEnum != OfferCreateFlags.TF_SELL:
                offer_create_request["flags"] = offer_create_request["flags"] | flagEnum

    if side == OrderSide.Sell:
        offer_create_request["flags"] = (
            offer_create_request["flags"] | OfferCreateFlags.TF_SELL.value
        )

    offer_create_response = safe_sign_and_submit_transaction(
        transaction=OfferCreate.from_dict(offer_create_request),
        wallet=self.wallet,
        client=self.sync_client,
    )
    offer_create_result = offer_create_response.result
    handle_response_error(offer_create_result)

    return CreateOrderResponse(
        id=OrderId(
            offer_create_result["tx_json"]["Account"],
            offer_create_result["tx_json"]["Sequence"],
        ),
        info={"OfferCreate": offer_create_result},
    )
