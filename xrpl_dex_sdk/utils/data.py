from typing import Any, Dict, List, Set

from ..models.xrpl.amounts import Amount
from ..models.xrpl.offers import OfferCreateFlags, OfferFlags
from ..models.common import MarketSymbol, CurrencyCode


def omit(d: Dict, keys: Set[str]):
    return {k: v for k, v in d.items() if k not in keys}


def sort_by_date(transaction: Dict[str, Any]):
    return transaction["tx"]["date"] if "tx" in transaction else transaction["date"]


def has_offer_flag(flags: int, target_flag: OfferFlags) -> bool:
    return flags & target_flag.value == target_flag.value


def has_offer_create_flag(flags: int, target_flag: OfferCreateFlags) -> bool:
    return flags & target_flag.value == target_flag.value


def get_market_symbol(base: Amount, quote: Amount) -> MarketSymbol:
    base_code = (
        CurrencyCode(currency="XRP")
        if isinstance(base, str)
        else CurrencyCode(currency=base["currency"], issuer=base["issuer"])
    )
    quote_code = (
        CurrencyCode(currency="XRP")
        if isinstance(quote, str)
        else CurrencyCode(currency=quote["currency"], issuer=quote["issuer"])
    )
    return MarketSymbol(base_code, quote_code)


__all__ = [
    "omit",
    "sort_by_date",
    "has_offer_flag",
    "has_offer_create_flag",
    "get_market_symbol",
]
