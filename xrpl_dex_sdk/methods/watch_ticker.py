import uuid
from typing import Any, Dict

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter

from ..models import (
    WatchTickerParams,
    MarketSymbol,
    Ticker,
)


async def watch_ticker(
    self,
    symbol: MarketSymbol,
    params: WatchTickerParams,
) -> None:
    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching balance: Websockets client not initialized")

    ticker: Ticker = None

    payload = Subscribe(
        id=uuid.uuid4().hex,
        streams=[StreamParameter.LEDGER],
    )

    async def ticker_handler(message: Any):
        if message["type"] == "transaction":
            if (
                message["validated"] == False
                or message["transaction"]["TransactionType"] != "OfferCreate"
            ):
                return

            new_ticker = await self.fetch_ticker(
                symbol, WatchTickerParams(search_limit=params.search_limit)
            )

            if new_ticker == None:
                return

            if ticker == None:
                return new_ticker
            else:
                for field in new_ticker._fields:
                    if field != "datetime" and field != "timestamp" and field != "info":
                        if new_ticker.__getattribute__(field) != ticker.__getattribute__(field):
                            return new_ticker

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

            new_ticker = await ticker_handler(message)
            if new_ticker != None:
                if isinstance(params, Dict):
                    params["listener"](new_ticker)
                else:
                    params.listener(new_ticker)
