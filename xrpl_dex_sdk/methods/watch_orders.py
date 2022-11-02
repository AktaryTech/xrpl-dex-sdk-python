from typing import Any, List, Optional, Dict
import uuid

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter

from ..models import (
    WatchOrdersParams,
    MarketSymbol,
    Offer,
    OrderId,
    Trade,
    Order,
    OrderStatus,
)
from ..utils import parse_transaction, get_order_from_data, get_trade_from_data


async def watch_orders(
    self,
    symbol: Optional[MarketSymbol],
    params: WatchOrdersParams,
) -> None:
    """
    Listens for new Orders for a single market pair.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        (Optional) Symbol to filter Orders by
    params : xrpl_dex_sdk.models.WatchOrdersParams
        Additional request parameters
    """

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching balance: Websockets client not initialized")

    payload = Subscribe(id=uuid.uuid4().hex, streams=[StreamParameter.TRANSACTIONS])

    async def orders_handler(tx_message: Any):
        if tx_message["type"] == "transaction":
            order_id = OrderId(
                account=tx_message["transaction"]["Account"],
                sequence=tx_message["transaction"]["Sequence"],
            )

            txn_data = parse_transaction(id=order_id, transaction=tx_message["transaction"])

            if txn_data == None or (symbol and symbol != order_id):
                return

            trades: List[Trade] = []
            order: Optional[Order] = None
            order_status = OrderStatus.Open
            filled: float = 0
            fill_price: float = 0
            total_fill_price: float = fill_price

            transaction = txn_data["transaction"]
            offers: List[Offer] = txn_data["offers"]
            date = txn_data["date"]

            for offer in offers:
                if offer.Sequence == None:
                    continue

                trade = await get_trade_from_data(
                    self,
                    {
                        "date": date,
                        "Flags": offer.Flags,
                        "OrderAccount": offer.Account,
                        "OrderSequence": offer.Sequence,
                        "Account": order_id.account,
                        "Sequence": order_id.sequence,
                        "TakerPays": offer.TakerPays,
                        "TakerGets": offer.TakerGets,
                    },
                    {"offer": offer},
                )

                if trade != None:
                    trades.append(trade)

            if (
                transaction["Account"] == order_id.account
                and transaction["Sequence"] == order_id.sequence
            ):
                source = transaction

                if "Sequence" not in source:
                    raise Exception("Couldn't find data for OrderId " + str(id))

                order = await get_order_from_data(
                    self,
                    {
                        "status": order_status,
                        "date": date,
                        "filled": filled,
                        "fill_price": fill_price,
                        "total_fill_price": total_fill_price,
                        "trades": trades,
                        "Flags": transaction["Flags"],
                        "Account": transaction["Account"],
                        "Sequence": transaction["Sequence"],
                        "TakerPays": transaction["TakerPays"],
                        "TakerGets": transaction["TakerGets"],
                    },
                    {"transaction_data": txn_data},
                )

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
                    params.listener(order)
                else:
                    params.listener(order)

    return
