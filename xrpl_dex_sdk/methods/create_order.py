from xrpl.utils import xrp_to_drops
from xrpl.transaction import safe_sign_and_submit_transaction
from xrpl.models.amounts.issued_currency_amount import IssuedCurrencyAmount
from xrpl.models.transactions import OfferCreate

from ..models.common import MarketSymbol
from ..models.ccxt.orders import OrderId, OrderSide, OrderType
from ..models.methods.create_order import CreateOrderParams, CreateOrderResponse
from ..models.xrpl import OfferCreateFlags
from ..utils.orders import get_base_amount_key


def create_order(
    self,
    symbol: MarketSymbol,
    side: OrderSide,
    # unused - always "limit"
    type: OrderType,
    amount: float,
    price: float,
    params: CreateOrderParams = CreateOrderParams(),
) -> CreateOrderResponse:
    base_amount = (
        IssuedCurrencyAmount(
            currency=symbol.base.currency,
            issuer=symbol.base.issuer,
            value=str(amount),
        )
        if symbol.base.issuer != None
        else xrp_to_drops(amount)
    )
    base_amount_key = get_base_amount_key(side)

    quote_amount = (
        IssuedCurrencyAmount(
            currency=symbol.quote.currency,
            issuer=symbol.quote.issuer,
            value=str(amount * price),
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

    for field in params._fields:
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
        client=self.client,
    )
    offer_create_result = offer_create_response.result

    if "error" in offer_create_result:
        raise Exception(
            offer_create_result["error"] + " " + offer_create_result["error_message"]
        )

    else:
        return CreateOrderResponse(
            id=OrderId(
                offer_create_result["tx_json"]["Account"],
                offer_create_result["tx_json"]["Sequence"],
            ),
            info={"OfferCreate": offer_create_result},
        )
