from typing import Any, Dict
import uuid

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter

from ..models import (
    WatchMyTradesParams,
    MarketSymbol,
)
from ..utils import (
    parse_affected_node,
    get_trade_from_data,
    get_market_symbol,
)


async def watch_my_trades(
    self,
    symbol: MarketSymbol,
    params: WatchMyTradesParams,
) -> None:
    """
    Listens for new Trades from the SDK user for a given market pair.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        Symbol to watch
    params : xrpl_dex_sdk.models.WatchMyTradesParams
        Additional request parameters
    """

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
                if node == None:
                    continue

                offer_fields = getattr(node, "FinalFields")
                if offer_fields == None:
                    continue

                trade = await get_trade_from_data(
                    self,
                    {
                        "date": transaction["date"],
                        "Flags": offer_fields["Flags"],
                        "OrderAccount": offer_fields["Account"],
                        "OrderSequence": offer_fields["Sequence"],
                        "Account": transaction["Account"],
                        "Sequence": transaction["Sequence"],
                        "TakerPays": offer_fields["TakerPays"],
                        "TakerGets": offer_fields["TakerGets"],
                    },
                    {"transaction": transaction},
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
                    params.listener(trade)
                else:
                    params.listener(trade)

    return
