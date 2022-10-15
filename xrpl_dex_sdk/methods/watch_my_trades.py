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
    parse_affected_node,
    get_base_amount_key,
    get_trade_from_data,
    get_quote_amount_key,
    parse_amount_value,
    get_taker_or_maker,
    get_market_symbol,
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

            if get_market_symbol(transaction) != symbol:
                return

            for affected_node in transaction["meta"]["AffectedNodes"]:
                node = parse_affected_node(affected_node)
                if node == None or "FinalFields" not in node:
                    continue

                offer = node["FinalFields"]

                trade = await get_trade_from_data(
                    self,
                    {
                        "date": transaction["date"],
                        "Flags": offer["Flags"],
                        "OrderAccount": offer["Account"],
                        "OrderSequence": offer["Sequence"],
                        "Account": transaction["Account"],
                        "Sequence": transaction["Sequence"],
                        "TakerPays": offer["TakerPays"],
                        "TakerGets": offer["TakerGets"],
                    },
                    {transaction},
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
