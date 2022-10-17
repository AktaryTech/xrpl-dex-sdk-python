import uuid
from typing import Any, Dict, List

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter

from ..models import (
    WatchTickersParams,
    MarketSymbol,
    OrderSide,
    OfferCreateFlags,
    Tickers,
)
from ..utils import (
    has_offer_create_flag,
    get_base_amount_key,
    get_quote_amount_key,
    get_market_symbol_from_amount,
)


async def watch_tickers(
    self,
    # Array of token pairs (called Unified Market Symbols in CCXT)
    symbols: List[MarketSymbol],
    params: WatchTickersParams,
) -> None:
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

            side = (
                OrderSide.Sell
                if has_offer_create_flag(transaction["Flags"], OfferCreateFlags.TF_SELL)
                else OrderSide.Buy
            )
            base_amount = transaction[get_base_amount_key(side)]
            quote_amount = transaction[get_quote_amount_key(side)]
            symbol = get_market_symbol_from_amount(base_amount, quote_amount)

            if symbol not in symbols:
                return

            new_ticker = await self.fetch_ticker(
                symbol,
                WatchTickersParams(
                    search_limit=params.search_limit, listener=params.listener
                ),
            )

            if new_ticker == None:
                return

            if symbol in tickers:
                for field in new_ticker._fields:
                    if field != "datetime" and field != "timestamp" and field != "info":
                        if new_ticker.__getattribute__(field) != tickers[
                            symbol
                        ].__getattribute__(field):
                            return new_ticker
            else:
                tickers[symbol] = new_ticker

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
