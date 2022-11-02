from typing import Any, Dict, Optional
import uuid

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, SubscribeBook

from ..constants import DEFAULT_LIMIT
from ..models import WatchOrderBookParams, MarketSymbol, IssuedCurrency, XRP


async def watch_order_book(
    self,
    symbol: MarketSymbol,
    limit: Optional[int],
    params: WatchOrderBookParams,
) -> None:
    """
    Listens for order book updates for a given market pair.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        Symbol to watch
    limit : int
        (Optional) Number of entries to return (default is to 20)
    params : xrpl_dex_sdk.models.WatchOrderBookParams
        Additional request parameters
    """

    limit = DEFAULT_LIMIT if limit == None else limit

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching balance: Websockets client not initialized")

    base_amount = (
        IssuedCurrency(currency=symbol.base.currency, issuer=symbol.base.issuer)
        if symbol.base.issuer != None
        else XRP()
    )

    quote_amount = (
        IssuedCurrency(currency=symbol.quote.currency, issuer=symbol.quote.issuer)
        if symbol.quote.issuer != None
        else XRP()
    )

    payload = Subscribe(
        id=uuid.uuid4().hex,
        books=[
            SubscribeBook(taker_pays=base_amount, taker_gets=quote_amount),
        ],
    )

    async def order_book_handler(message: Any):
        print("\nGot message!\n")
        print(message)
        if message["type"] == "transaction":
            if (
                message["validated"] != True
                or message["transaction"]["TransactionType"] != "OfferCreate"
            ):
                return
            return await self.fetch_order_book(symbol, limit)

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

            order_book = await order_book_handler(message)
            if order_book != None:
                if isinstance(params, Dict):
                    params.listener(order_book)
                else:
                    params.listener(order_book)

    return
