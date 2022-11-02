from typing import Optional, Union
from time import time
from datetime import datetime

from xrpl.models.requests.book_offers import BookOffers

from ..constants import CURRENCY_PRECISION, DEFAULT_TICKER_SEARCH_LIMIT
from ..models import (
    FetchTickerParams,
    BookOffer,
    FetchTickerResponse,
    MarketSymbol,
    Ticker,
)
from ..utils import (
    handle_response_error,
    sort_by_previous_txn_lgr_seq,
    get_book_offer_base_value,
    get_book_offer_quote_value,
)


async def fetch_ticker(
    self, symbol: MarketSymbol, params: FetchTickerParams = FetchTickerParams()
) -> Optional[FetchTickerResponse]:
    """
    Retrieves price ticker data for a single market pair.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        Market symbol to get price ticker data for
    params : xrpl_dex_sdk.models.FetchTickerParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchTickerResponse
        Price ticker data
    """

    search_limit = params.search_limit if params.search_limit else DEFAULT_TICKER_SEARCH_LIMIT

    high: Union[float, None] = None
    low: Union[float, None] = None

    bid: Union[float, None] = None
    bid_volume: Union[float, None] = None
    ask: Union[float, None] = None
    ask_volume: Union[float, None] = None

    vwap_price: float = 0
    vwap_quantity: float = 0

    base_volume: float = 0
    quote_volume: float = 0

    base_amount = {"currency": symbol.base.currency}
    if symbol.base.issuer:
        base_amount["issuer"] = symbol.base.issuer

    quote_amount = {"currency": symbol.quote.currency}
    if symbol.quote.issuer:
        quote_amount["issuer"] = symbol.quote.issuer

    bids_response = await self.client.request(
        BookOffers.from_dict(
            {
                "limit": search_limit + 1,
                "taker_pays": base_amount,
                "taker_gets": quote_amount,
            }
        )
    )
    bids_result = bids_response.result
    handle_response_error(bids_result)

    asks_response = await self.client.request(
        BookOffers.from_dict(
            {
                "limit": search_limit + 1,
                "taker_pays": quote_amount,
                "taker_gets": base_amount,
            }
        )
    )
    asks_result = asks_response.result
    handle_response_error(asks_result)

    book_offers = bids_result["offers"] + asks_result["offers"]

    book_offers.sort(reverse=False, key=sort_by_previous_txn_lgr_seq)

    def get_book_offer_price(book_offer: BookOffer) -> float:
        return get_book_offer_quote_value(book_offer) / get_book_offer_base_value(book_offer)

    open = get_book_offer_price(BookOffer.from_dict(book_offers[1]))
    close = get_book_offer_price(BookOffer.from_dict(book_offers[-1]))
    previous_close = get_book_offer_price(BookOffer.from_dict(book_offers[0]))

    for book_offer_dict in book_offers:
        book_offer = BookOffer.from_dict(book_offer_dict)
        book_offer_price = get_book_offer_price(book_offer)

        if not high or book_offer_price > high:
            high = book_offer_price
        if not low or book_offer_price < low:
            low = book_offer_price

        base_value = get_book_offer_base_value(book_offer)
        quote_value = get_book_offer_quote_value(book_offer)

        if not bid or book_offer_price > bid:
            bid = book_offer_price
        if not bid_volume or base_value > bid_volume:
            bid_volume = base_value

        if not ask or book_offer_price > ask:
            ask = book_offer_price
        if not ask_volume or quote_value > ask_volume:
            ask_volume = quote_value

        base_volume += base_value
        quote_volume += quote_value

        vwap_price += book_offer_price * base_value
        vwap_quantity += base_value

    vwap = vwap_price / vwap_quantity
    change = close - open
    percentage = change / open * 100
    average = (close + open) / 2

    timestamp = round(time())
    iso_timestamp = datetime.fromtimestamp(timestamp).isoformat()

    ticker = Ticker(
        symbol=symbol,
        timestamp=timestamp,
        datetime=iso_timestamp,
        high=round(high if high else 0, CURRENCY_PRECISION),
        low=round(low if low else 0, CURRENCY_PRECISION),
        bid=round(bid if bid else 0, CURRENCY_PRECISION),
        bid_volume=round(bid_volume if bid_volume else 0, CURRENCY_PRECISION),
        ask=round(ask if ask else 0, CURRENCY_PRECISION),
        ask_volume=round(ask_volume if ask_volume else 0, CURRENCY_PRECISION),
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
