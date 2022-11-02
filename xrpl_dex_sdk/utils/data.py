from typing import Any, Dict, Set

from ..models.xrpl.offers import OfferCreateFlags, OfferFlags


def omit(d: Dict, keys: Set[str]):
    """Omits the contents of the `keys` set from the dictionary."""
    return {k: v for k, v in d.items() if k not in keys}


#
# Sorting
#
def sort_by_date(transaction: Dict[str, Any]):
    """Sorts Transactions by their dates."""
    return transaction["tx"]["date"] if "tx" in transaction else transaction["date"]


def sort_by_previous_txn_lgr_seq(offer: Dict[str, Any]):
    """Sorts Offers by their PreviousTxnLgrSeq values."""
    return offer["PreviousTxnLgrSeq"]


#
# Offer Flags
#


def has_offer_flag(flags: int, target_flag: OfferFlags) -> bool:
    """Returns true if a given Offer flag is present on an Offer."""
    return flags & target_flag.value == target_flag.value


def has_offer_create_flag(flags: int, target_flag: OfferCreateFlags) -> bool:
    """Returns true if a given OfferCreate flag is present on an Offer."""
    return flags & target_flag.value == target_flag.value
