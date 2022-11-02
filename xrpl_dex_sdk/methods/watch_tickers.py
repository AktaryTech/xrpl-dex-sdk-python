import uuid
from typing import Any, Dict, List, Set, cast

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter

from ..models import (
    WatchTickersParams,
    MarketSymbol,
    Tickers,
)
from ..utils import (
    get_market_symbol,
    omit,
)


async def watch_tickers(
    self,
    # Array of token pairs (called Unified Market Symbols in CCXT)
    symbols: List[MarketSymbol],
    params: WatchTickersParams,
) -> None:
    """
    Listens for new price ticker data for multiple market pairs.

    Parameters
    ----------
    symbols : List[xrpl_dex_sdk.models.MarketSymbol]
        List of market symbols to get price ticker data for
    params : xrpl_dex_sdk.models.WatchTickersParams
        Additional request parameters
    """

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching balance: Websockets client not initialized")

    tickers: Tickers = {}

    payload = Subscribe(
        id=uuid.uuid4().hex,
        streams=[StreamParameter.TRANSACTIONS],
    )

    async def tickers_handler(message: Any):
        if message["type"] == "transaction":
            if (
                message["validated"] == False
                or message["transaction"]["TransactionType"] != "OfferCreate"
            ):
                return

            transaction = message["transaction"]

            symbol = get_market_symbol(transaction)

            if symbol == None or symbol not in symbols:
                return

            new_ticker = await self.fetch_ticker(symbol, params)

            if new_ticker == None:
                return

            if symbol in tickers:
                omitted_fields = cast(Set, ["datetime", "timestamp", "info"])
                if omit(tickers[symbol].to_dict(), omitted_fields) != omit(
                    new_ticker.to_dict(), omitted_fields
                ):
                    tickers[symbol] = new_ticker
                    return new_ticker
            else:
                tickers[symbol] = new_ticker
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

            new_ticker = await tickers_handler(message)
            if new_ticker != None:
                if isinstance(params, Dict):
                    params.listener(new_ticker)
                else:
                    params.listener(new_ticker)
