from typing import Any, Dict, Set

from ..models.xrpl.offers import OfferCreateFlags, OfferFlags


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


__all__ = [
    "omit",
    "sort_by_date",
    "sort_by_previous_txn_lgr_seq",
    "has_offer_flag",
    "has_offer_create_flag",
]
