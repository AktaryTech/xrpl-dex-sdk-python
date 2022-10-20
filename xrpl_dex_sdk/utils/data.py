import json
from typing import Any, Callable, Dict, List, Set, Tuple

from xrpl.clients import WebsocketClient

from ..models.xrpl.common import Amount
from ..models.xrpl.offers import OfferCreateFlags, OfferFlags
from ..models.common import MarketSymbol, CurrencyCode


def omit(d: Dict, keys: Set[str]):
    return {k: v for k, v in d.items() if k not in keys}


#
# Sorting
#
def sort_by_date(transaction: Dict[str, Any]):
    return transaction["tx"]["date"] if "tx" in transaction else transaction["date"]


def sort_by_previous_txn_lgr_seq(offer: Dict[str, Any]):
    return offer["PreviousTxnLgrSeq"]


#
# Offer Flags
#


def has_offer_flag(flags: int, target_flag: OfferFlags) -> bool:
    return flags & target_flag.value == target_flag.value


def has_offer_create_flag(flags: int, target_flag: OfferCreateFlags) -> bool:
    return flags & target_flag.value == target_flag.value


def get_market_symbol(base: Amount, quote: Amount) -> MarketSymbol:
    base_code = (
        CurrencyCode("XRP")
        if isinstance(base, str)
        else CurrencyCode(base["currency"], base["issuer"])
    )
    quote_code = (
        CurrencyCode("XRP")
        if isinstance(quote, str)
        else CurrencyCode(quote["currency"], quote["issuer"])
    )
    return MarketSymbol(base_code.code, quote_code.code)


#
# Subscriptions
#
async def subscribe(
    self, payload: str, listener: Callable, transform: Callable, extra: Tuple
) -> None:
    """subscribes to stream"""
    async with WebsocketClient(self.ws_url) as websocket:
        print(json.dumps(json.loads(payload), indent=4))
        await websocket.send(payload)
        initialized = False
        async for message in websocket:
            json_message = json.loads(message)
            if initialized is False:
                print(json.dumps(json_message, indent=4))
                if json_message.get("status") == "success":
                    initialized = True
                    continue
                else:
                    raise Exception(message)

            listener(json_message)

            # # call function passed in with data
            # transformed = transform(json_message, extra)
            # # return none from transformed to prevent message callback
            # if transformed:
            #     listener(transformed)


__all__ = [
    "omit",
    "sort_by_date",
    "sort_by_previous_txn_lgr_seq",
    "has_offer_flag",
    "has_offer_create_flag",
    "get_market_symbol",
    "subscribe",
]
