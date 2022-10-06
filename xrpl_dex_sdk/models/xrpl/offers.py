from enum import Enum
from typing import NamedTuple, Optional

from ..common import XrplTimestamp
from .amounts import Amount
from .ledger import LedgerEntryTypes


class Offer(NamedTuple):
    index: str
    LedgerEntryType: LedgerEntryTypes
    Flags: int
    Account: str
    Sequence: int
    TakerPays: Amount
    TakerGets: Amount
    BookDirectory: str
    BookNode: str
    OwnerNode: str
    PreviousTxnID: str
    PreviousTxnLgrSeq: int
    Expiration: Optional[XrplTimestamp]


class OfferFlags(Enum):
    LSF_PASSIVE: int = 65536
    LSF_SELL: int = 131072


class OfferCreateFlags(Enum):
    TF_FILL_OR_KILL: int = 262144
    TF_IMMEDIATE_OR_CANCEL: int = 131072
    TF_PASSIVE: int = 65536
    TF_SELL: int = 524288
