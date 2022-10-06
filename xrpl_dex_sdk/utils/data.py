from typing import Any, Dict, Set

from ..models.xrpl.offers import OfferCreateFlags, OfferFlags


def omit(d: Dict, keys: Set[str]):
    return {k: v for k, v in d.items() if k not in keys}


def sort_by_date(transaction: Dict[str, Any]):
    return transaction["tx"]["date"] if "tx" in transaction else transaction["date"]


def has_offer_flag(flags: int, target_flag: OfferFlags) -> bool:
    return flags & target_flag.value == target_flag.value


def has_offer_create_flag(flags: int, target_flag: OfferCreateFlags) -> bool:
    return flags & target_flag.value == target_flag.value
