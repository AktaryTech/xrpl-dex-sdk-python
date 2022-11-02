import uuid
from typing import Any, Dict, Optional, Set, cast

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter

from ..models import (
    WatchTickerParams,
    MarketSymbol,
    Ticker,
)
from ..utils import omit


async def watch_ticker(
    self,
    symbol: MarketSymbol,
    params: WatchTickerParams,
) -> None:
    """
    Listens for new price ticker data for a single market pair.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        Market symbol to get price ticker data for
    params : xrpl_dex_sdk.models.WatchTickerParams
        Additional request parameters
    """

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching balance: Websockets client not initialized")

    ticker: Optional[Ticker] = None

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

            new_ticker: Optional[Ticker] = await self.fetch_ticker(symbol, params)

            if new_ticker == None:
                return

            if ticker == None:
                return new_ticker
            else:
                omitted_fields = cast(Set, ["datetime", "timestamp", "info"])
                return (
                    new_ticker
                    if omit(ticker.to_dict(), omitted_fields)
                    != omit(new_ticker.to_dict(), omitted_fields)
                    else None
                )

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
                ticker = new_ticker
                if isinstance(params, Dict):
                    params.listener(new_ticker)
                else:
                    params.listener(new_ticker)
