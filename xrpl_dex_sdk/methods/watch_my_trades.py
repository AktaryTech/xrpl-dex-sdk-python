from pprint import pprint
from typing import Any, Callable, Dict
import uuid

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime, ripple_time_to_posix

from ..constants import CURRENCY_PRECISION
from ..models import (
    WatchMyTradesParams,
    OrderSide,
    Offer,
    MarketSymbol,
    TradeId,
    OrderId,
    Trade,
    TradeType,
)
from ..utils import (
    get_amount_currency_code,
    get_order_side,
    get_market_symbol,
    get_base_amount_key,
    get_quote_amount_key,
    fetch_transfer_rate,
    parse_amount_value,
    get_taker_or_maker,
)


async def watch_my_trades(
    self,
    # Market symbol to fetch trades for
    symbol: MarketSymbol,
    params: WatchMyTradesParams,
) -> None:
    symbol = MarketSymbol(symbol) if isinstance(symbol, str) else symbol

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching trades: Websockets client not initialized")

    account = self.wallet.classic_address
    payload = Subscribe(
        id=uuid.uuid4().hex,
        accounts=[account],
        streams=[StreamParameter.TRANSACTIONS],
    )

    async def my_trades_handler(message: Any):
        if message["type"] == "transaction":
            transaction = message["transaction"]
            if (
                transaction == None
                or transaction["TransactionType"] != "OfferCreate"
                or "meta" not in transaction
                or "Sequence" not in transaction
                or transaction["Account"] != account
            ):
                return

            side = get_order_side(transaction["Flags"])

            market_symbol = get_market_symbol(
                transaction[get_base_amount_key(side)],
                transaction[get_quote_amount_key(side)],
            )

            if market_symbol != symbol:
                return

            for affected_node in transaction["meta"]["AffectedNodes"]:
                node = (
                    affected_node["ModifiedNode"]
                    if "ModifiedNode" in affected_node
                    else affected_node["DeletedNode"]
                    if "DeletedNode" in affected_node
                    else None
                )

                if node == None or node["LedgerEntryType"] != "Offer" or "FinalFields" not in node:
                    continue

                offer: Offer = node["FinalFields"]

                base_amount = offer[get_base_amount_key(side)]
                base_currency = get_amount_currency_code(base_amount)
                base_rate = await fetch_transfer_rate(self.client, base_currency)
                base_amount_value = parse_amount_value(base_amount)
                base_value = (
                    float(drops_to_xrp(str(base_amount_value)))
                    if base_currency == "XRP"
                    else base_amount_value
                )
                if base_value == 0:
                    continue

                quote_amount = offer[get_quote_amount_key(side)]
                quote_currency = get_amount_currency_code(quote_amount)
                quote_rate = await fetch_transfer_rate(self.client, quote_currency)
                quote_amount_value = parse_amount_value(quote_amount)
                quote_value = (
                    float(drops_to_xrp(str(quote_amount_value)))
                    if quote_currency == "XRP"
                    else quote_amount_value
                )
                if quote_value == 0:
                    continue

                amount = base_value
                price = quote_value / amount
                cost = amount * price

                fee_rate = quote_rate if side == OrderSide.Buy else base_rate
                fee_cost = (quote_value if side == OrderSide.Buy else base_value) * fee_rate

                trade = Trade(
                    id=TradeId(transaction["Account"], transaction["Sequence"]),
                    order=OrderId(offer["Account"], offer["Sequence"]),
                    datetime=ripple_time_to_datetime(transaction["date"] or 0),
                    timestamp=ripple_time_to_posix(transaction["date"] or 0),
                    symbol=MarketSymbol(base_currency.code, quote_currency.code).symbol,
                    type=TradeType.Limit.value,
                    side=side,
                    amount=round(amount, CURRENCY_PRECISION),
                    price=round(price, CURRENCY_PRECISION),
                    takerOrMaker=get_taker_or_maker(side).value,
                    cost=round(cost, CURRENCY_PRECISION),
                    fee={
                        "currency": str(base_currency if side == OrderSide.Buy else quote_currency),
                        "cost": round(fee_cost, CURRENCY_PRECISION),
                        "rate": round(fee_rate, CURRENCY_PRECISION),
                        "percentage": True,
                    }
                    if fee_cost > 0
                    else None,
                    info={"transaction": transaction},
                )

                return trade

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

            trade = await my_trades_handler(message)
            if trade != None:
                if isinstance(params, Dict):
                    params["listener"](trade)
                else:
                    params.listener(trade)

    return {}
