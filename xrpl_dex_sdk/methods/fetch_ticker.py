from typing import Any, Dict

from xrpl.models.requests.book_offers import BookOffers

from ..constants import CURRENCY_PRECISION
from ..models import (
    FetchTickerParams,
    FetchTickerResponse,
    MarketSymbol,
    Ticker,
)
from ..utils import (
    sort_by_previous_txn_lgr_seq,
    get_book_offer_base_value,
    get_book_offer_quote_value,
)


async def fetch_ticker(
    self,
    symbol: MarketSymbol,
    params: FetchTickerParams = FetchTickerParams(),
) -> FetchTickerResponse:
    symbol = MarketSymbol(symbol) if isinstance(symbol, str) == True else symbol

    high: float = None
    low: float = None

    bid: float = None
    bid_volume: float = None
    ask: float = None
    ask_volume: float = None

    vwap_price: float = 0
    vwap_quantity: float = 0

    base_volume: float = 0
    quote_volume: float = 0

    base_amount = {"currency": symbol.base.currency}
    if symbol.base.issuer != None:
        base_amount["issuer"] = symbol.base.issuer

    quote_amount = {"currency": symbol.quote.currency}
    if symbol.quote.issuer != None:
        quote_amount["issuer"] = symbol.quote.issuer

    bids_response = await self.client.request(
        BookOffers.from_dict(
            {
                "limit": params.search_limit + 1,
                "taker_pays": base_amount,
                "taker_gets": quote_amount,
            }
        )
    )
    bids_result = bids_response.result
    if "error" in bids_result:
        raise Exception(bids_result["error"] + " " + bids_result["error_message"])

    asks_response = await self.client.request(
        BookOffers.from_dict(
            {
                "limit": params.search_limit + 1,
                "taker_pays": quote_amount,
                "taker_gets": base_amount,
            }
        )
    )
    asks_result = asks_response.result
    if "error" in asks_result:
        raise Exception(asks_result["error"] + " " + asks_result["error_message"])

    book_offers = bids_result["offers"] + asks_result["offers"]

    book_offers.sort(reverse=False, key=sort_by_previous_txn_lgr_seq)

    def get_book_offer_price(book_offer: Dict[str, Any]) -> float:
        return get_book_offer_quote_value(book_offer) / get_book_offer_base_value(book_offer)

    open = get_book_offer_price(book_offers[1])
    close = get_book_offer_price(book_offers[len(book_offers) - 1])
    previous_close = get_book_offer_price(book_offers[0])

    for book_offer in book_offers:
        price = get_book_offer_price(book_offer)

        if high == None or price > high:
            high = price
        if low == None or price < low:
            low = price

        base_value = get_book_offer_base_value(book_offer)
        quote_value = get_book_offer_quote_value(book_offer)

        if bid == None or price > bid:
            bid = price
        if bid_volume == None or base_value > bid_volume:
            bid_volume = base_value

        if ask == None or price > ask:
            ask = price
        if ask_volume == None or quote_value > ask_volume:
            ask_volume = quote_value

        base_volume += base_value
        quote_volume += quote_value

        vwap_price += price * base_value
        vwap_quantity += base_value

    vwap = vwap_price / vwap_quantity
    change = close - open
    percentage = change / open * 100
    average = (close + open) / 2

    ticker = Ticker(
        symbol=symbol,
        timestamp=None,
        datetime=None,
        high=round(high, CURRENCY_PRECISION),
        low=round(low, CURRENCY_PRECISION),
        bid=round(bid, CURRENCY_PRECISION),
        bid_volume=round(bid_volume, CURRENCY_PRECISION),
        ask=round(ask, CURRENCY_PRECISION),
        ask_volume=round(ask_volume, CURRENCY_PRECISION),
        vwap=round(vwap, CURRENCY_PRECISION),
        open=round(open, CURRENCY_PRECISION),
        close=round(close, CURRENCY_PRECISION),
        last=round(close, CURRENCY_PRECISION),
        previous_close=round(previous_close, CURRENCY_PRECISION),
        change=round(change, CURRENCY_PRECISION),
        percentage=round(percentage, CURRENCY_PRECISION),
        average=round(average, CURRENCY_PRECISION),
        base_volume=round(base_volume, CURRENCY_PRECISION),
        quote_volume=round(quote_volume, CURRENCY_PRECISION),
        info={"bids": bids_result, "asks": asks_result},
    )

    return ticker
