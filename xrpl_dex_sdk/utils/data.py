from typing import Any, Dict, List, Set

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


__all__ = [
    "omit",
    "sort_by_date",
    "sort_by_previous_txn_lgr_seq",
    "has_offer_flag",
    "has_offer_create_flag",
    "get_market_symbol",
]
