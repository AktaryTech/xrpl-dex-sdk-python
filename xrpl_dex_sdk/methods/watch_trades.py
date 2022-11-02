from typing import Any, Dict
import uuid

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter

from ..models import (
    WatchTradesParams,
    Trades,
    MarketSymbol,
)
from ..utils import (
    get_market_symbol,
    parse_affected_node,
    get_trade_from_data,
)


async def watch_trades(
    self,
    # Market symbol to fetch trades for
    symbol: MarketSymbol,
    params: WatchTradesParams,
) -> None:
    """
    Listens for new Trades for a given market symbol.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        (Optional) Market symbol to filter Trades by
    params : xrpl_dex_sdk.models.WatchTradesParams
        Additional request parameters
    """

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching trades: Websockets client not initialized")

    payload = Subscribe(
        id=uuid.uuid4().hex,
        streams=[StreamParameter.TRANSACTIONS],
    )

    async def trades_handler(message: Any):
        if message["type"] == "transaction":
            transaction = message["transaction"] if "transaction" in message else None
            metadata = message["meta"] if "meta" in message else None
            if (
                not transaction
                or not metadata
                or "Sequence" not in transaction
                or transaction["TransactionType"] != "OfferCreate"
            ):
                return

            if get_market_symbol(transaction) != symbol:
                return

            trades: Trades = []

            for affected_node in metadata["AffectedNodes"]:
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

                if trade:
                    trades.append(trade)

            return trades if len(trades) else None

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

            trades = await trades_handler(message)
            if trades:
                if isinstance(params, Dict):
                    params["listener"](trades)
                else:
                    params.listener(trades)

    return
