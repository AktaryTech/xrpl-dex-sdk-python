from typing import Any, Dict, Optional
import uuid

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, SubscribeBook

from ..constants import DEFAULT_LIMIT
from ..models import WatchOrderBookParams, MarketSymbol, IssuedCurrency, XRP


async def watch_order_book(
    self,
    # Token pair (called Unified Market Symbol in CCXT)
    symbol: MarketSymbol,
    # Number of results to return in book
    limit: Optional[int],
    params: WatchOrderBookParams,
) -> None:
    # symbol = MarketSymbol.from_string(symbol) if isinstance(symbol, str) else symbol
    limit = DEFAULT_LIMIT if limit == None else limit

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching balance: Websockets client not initialized")

    base_amount = (
        IssuedCurrency(currency=symbol.base.currency, issuer=symbol.base.issuer)
        if symbol.base.issuer != None
        else XRP()
    )
    # if symbol.base.issuer != None:
    #     base_amount["issuer"] = symbol.base.issuer

    quote_amount = (
        IssuedCurrency(currency=symbol.quote.currency, issuer=symbol.quote.issuer)
        if symbol.quote.issuer != None
        else XRP()
    )

    # quote_amount = {"currency": symbol.quote.currency}
    # if symbol.quote.issuer != None:
    #     quote_amount["issuer"] = symbol.quote.issuer

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
