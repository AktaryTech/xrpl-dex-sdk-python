from typing import List

from xrpl.models.requests.book_offers import BookOffers
from xrpl.utils import drops_to_xrp

from ..constants import DEFAULT_LIMIT
from ..models import (
    FetchOrderBookParams,
    FetchOrderBookResponse,
    OrderBook,
    OrderBookEntry,
    OrderBookLevel,
    OfferFlags,
    OrderSide,
    MarketSymbol,
)
from ..utils import handle_response_error


async def fetch_order_book(
    self,
    symbol: MarketSymbol,
    limit: int = DEFAULT_LIMIT,
    params: FetchOrderBookParams = FetchOrderBookParams(),
) -> FetchOrderBookResponse:
    """
    Retrieves order book data for a single market pair.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        Market symbol to get order book for
    limit : int
        (Optional) Total number of entries to return (default is 20)
    params : xrpl_dex_sdk.models.FetchOrderBookParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchOrderBookResponse
        Order book
    """

    taker_pays = {
        "currency": symbol.base.currency,
    }

    if symbol.base.issuer != None:
        taker_pays["issuer"] = symbol.base.issuer

    taker_gets = {
        "currency": symbol.quote.currency,
    }

    if symbol.quote.issuer != None:
        taker_gets["issuer"] = symbol.quote.issuer

    book_offers_request = {
        "taker_pays": taker_pays,
        "taker_gets": taker_gets,
        "limit": params.search_limit,
        "ledger_index": params.ledger_index if params.ledger_index != None else "validated",
    }

    if params.ledger_hash != None:
        book_offers_request["ledger_hash"] = params.ledger_hash
    if params.taker != None:
        book_offers_request["taker"] = params.taker

    book_offers_response = await self.client.request(BookOffers.from_dict(book_offers_request))
    book_offers_result = book_offers_response.result
    handle_response_error(book_offers_result)

    offers = book_offers_result["offers"]
    level: OrderBookLevel = OrderBookLevel.L2
    bids: List[OrderBookEntry] = []
    asks: List[OrderBookEntry] = []
    nonce = 0

    for offer in offers:

        side: OrderSide = (
            OrderSide.Sell
            if offer["Flags"] & OfferFlags.LSF_SELL.value == OfferFlags.LSF_SELL.value
            else OrderSide.Buy
        )

        base_amount = offer["TakerPays"] if side == OrderSide.Buy else offer["TakerGets"]
        base_value = float(
            base_amount["value"] if "value" in base_amount else drops_to_xrp(base_amount)
        )

        quote_amount = offer["TakerGets"] if side == OrderSide.Buy else offer["TakerPays"]
        quote_value = float(
            quote_amount["value"] if "value" in quote_amount else drops_to_xrp(quote_amount)
        )

        order_book_entry = [quote_value / base_value, base_value]

        if side == OrderSide.Buy:
            bids.append(order_book_entry)
        else:
            asks.append(order_book_entry)

        nonce = offer["Sequence"]

        if len(bids) + len(asks) >= limit:
            break

    return OrderBook(symbol=symbol, nonce=nonce, bids=bids, asks=asks, level=level)
