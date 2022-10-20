from typing import Any, List, Optional, Dict
import uuid

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime, ripple_time_to_posix

from ..constants import CURRENCY_PRECISION
from ..models import (
    WatchOrdersParams,
    MarketSymbol,
    Offer,
    Node,
    OrderId,
    Trades,
    Trade,
    TradeSide,
    TradeType,
    CurrencyCode,
    Order,
    OrderType,
    OfferCreateFlags,
    OrderStatus,
    OfferFlags,
    OrderSide,
    XrplTimestamp,
)
from ..utils import (
    get_offer_from_node,
    get_base_amount_key,
    get_quote_amount_key,
    get_market_symbol,
    get_order_time_in_force,
    fetch_transfer_rate,
    parse_amount_value,
    has_offer_create_flag,
    hash_offer_id,
    has_offer_flag,
    get_taker_or_maker,
)


async def watch_orders(
    self,
    # Token pair (called Unified Market Symbol in CCXT)
    symbol: Optional[MarketSymbol],
    params: WatchOrdersParams,
) -> None:
    symbol = MarketSymbol(symbol) if isinstance(symbol, str) else symbol

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching balance: Websockets client not initialized")

    payload = Subscribe(id=uuid.uuid4().hex, streams=[StreamParameter.TRANSACTIONS])

    async def orders_handler(message: Any):
        if message["type"] == "transaction":
            if (
                message["validated"] != True
                or message["transaction"]["TransactionType"] != "OfferCreate"
            ):
                return

            transaction = message["transaction"]

            if transaction == None or "Sequence" not in transaction:
                return

            trade_offers: List[Offer] = []

            for affected_node in message["meta"]["AffectedNodes"]:
                offer = get_offer_from_node(affected_node)
                if offer != None and offer.Account != transaction["Account"]:
                    trade_offers.append(offer)

            order_id = OrderId(transaction["Account"], transaction["Sequence"])
            trades: Trades = []
            date: XrplTimestamp = transaction["date"]
            order: Order = None
            order_status: OrderStatus = OrderStatus.Open
            filled: float = 0
            fill_price: float = 0
            total_fill_price = fill_price

            order_side = (
                OrderSide.Sell
                if has_offer_create_flag(transaction["Flags"], OfferCreateFlags.TF_SELL)
                else OrderSide.Buy
            )
            order_base_amount = transaction[get_base_amount_key(order_side)]
            order_quote_amount = transaction[get_quote_amount_key(order_side)]
            order_symbol = get_market_symbol(order_base_amount, order_quote_amount)

            if symbol != None and symbol != order_symbol:
                return

            for offer in trade_offers:
                side: TradeSide = (
                    TradeSide.Sell.value
                    if has_offer_flag(offer.Flags, OfferFlags.LSF_SELL)
                    else TradeSide.Buy.value
                )

                base_amount = offer.TakerPays if side == TradeSide.Buy.value else offer.TakerGets
                base_code = (
                    CurrencyCode(base_amount["currency"], base_amount["issuer"])
                    if "currency" in base_amount
                    else CurrencyCode("XRP")
                )
                base_amount_value = parse_amount_value(base_amount)
                base_value = (
                    float(drops_to_xrp(str(base_amount_value)))
                    if isinstance(base_amount_value, int)
                    else base_amount_value
                )

                quote_amount = offer.TakerGets if side == TradeSide.Buy.value else offer.TakerPays
                quote_code = (
                    CurrencyCode(quote_amount["currency"], quote_amount["issuer"])
                    if "currency" in quote_amount
                    else CurrencyCode("XRP")
                )
                quote_rate = await fetch_transfer_rate(self.client, quote_code)
                quote_amount_value = parse_amount_value(quote_amount)
                quote_value = (
                    float(drops_to_xrp(str(quote_amount_value)))
                    if isinstance(quote_amount_value, int)
                    else quote_amount_value
                )

                amount = base_value
                price = quote_value / amount
                cost = amount * price

                fee_rate = quote_rate
                fee_cost = quote_value * fee_rate

                filled = filled + amount
                fill_price = price
                total_fill_price = total_fill_price + fill_price

                # trade_info: Dict[str, Any] = {}
                # if transaction["Account"] != id.account:
                #     trade_info["transaction"] = offer
                # else:
                #     trade_info["offer"] = offer

                trade = Trade(
                    id=OrderId(offer.Account, offer.Sequence).id,
                    order=id.id,
                    datetime=ripple_time_to_datetime(date or 0),
                    timestamp=ripple_time_to_posix(date or 0),
                    symbol=MarketSymbol(base_code.code, quote_code.code).symbol,
                    type=TradeType.Limit.value,
                    side=side,
                    amount=round(amount, CURRENCY_PRECISION),
                    price=round(price, CURRENCY_PRECISION),
                    takerOrMaker=get_taker_or_maker(side).value,
                    cost=round(cost, CURRENCY_PRECISION),
                    fee={
                        "currency": str(quote_code),
                        "cost": round(fee_cost, CURRENCY_PRECISION),
                        "rate": round(fee_rate, CURRENCY_PRECISION),
                        "percentage": True,
                    }
                    if fee_cost > 0
                    else None,
                    info={"offer": offer},
                )
                trades.append(trade)

            order_time_in_force = get_order_time_in_force(transaction)

            order_base_rate = await fetch_transfer_rate(self.client, order_symbol.base)
            order_base_amount_value = parse_amount_value(order_base_amount)
            order_base_value = (
                float(drops_to_xrp(str(order_base_amount_value)))
                if isinstance(order_base_amount_value, int)
                else order_base_amount_value
            )
            order_quote_rate = await fetch_transfer_rate(self.client, order_symbol.quote)
            order_quote_amount_value = parse_amount_value(order_quote_amount)
            order_quote_value = (
                float(drops_to_xrp(str(order_quote_amount_value)))
                if isinstance(order_quote_amount_value, int)
                else order_quote_amount_value
            )

            order_amount = order_base_value
            order_price = order_quote_value / order_amount
            order_actual_price = fill_price

            order_average = total_fill_price / len(trades) if len(trades) > 0 else float(0)

            order_remaining = order_amount - filled
            order_cost = filled * order_actual_price

            order_fee_rate = order_quote_rate if order_side == OrderSide.Buy else order_base_rate
            order_fee_cost = filled * order_fee_rate

            order = Order(
                id=order_id,
                clientOrderId=hash_offer_id(transaction["Account"], transaction["Sequence"]),
                datetime=ripple_time_to_datetime(date or 0),
                timestamp=ripple_time_to_posix(date or 0),
                lastTradeTimestamp=ripple_time_to_posix(date or 0),
                status=order_status,
                symbol=order_symbol,
                type=OrderType.Limit.value,
                timeInForce=order_time_in_force,
                side=order_side,
                amount=round(order_amount, CURRENCY_PRECISION),
                price=round(order_price, CURRENCY_PRECISION),
                average=round(order_average, CURRENCY_PRECISION),
                filled=round(filled, CURRENCY_PRECISION),
                remaining=round(order_remaining, CURRENCY_PRECISION),
                cost=round(order_cost, CURRENCY_PRECISION),
                trades=trades,
                fee={
                    "currency": order_symbol.quote
                    if order_side == OrderSide.Buy
                    else order_symbol.base,
                    "cost": round(order_fee_cost, CURRENCY_PRECISION),
                    "rate": round(order_fee_rate, CURRENCY_PRECISION),
                    "percentage": True,
                }
                if order_fee_cost > 0
                else None,
                info={"transaction": message},
            )

            if (
                order.status == OrderStatus.Open.value
                and params.show_open == False
                or order.status == OrderStatus.Closed.value
                and params.show_closed == False
                or order.status == OrderStatus.Canceled.value
                and params.show_canceled == False
            ):
                return

            return order

    async with self.websocket_client as websocket:
        await websocket.send(payload)
        initialized = False
        async for message in websocket:
            if initialized is False:
                if message.get("status") == "success":
                    initialized = True
                    continue
                else:
                    raise Exception(message)

            order = await orders_handler(message)
            if order != None:
                if isinstance(params, Dict):
                    params["listener"](order)
                else:
                    params.listener(order)

    return {}
