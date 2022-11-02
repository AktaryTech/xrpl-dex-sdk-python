from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ..common import XrplTimestamp
from ..xrpl.currency import Amount
from .ledger import LedgerEntryTypes
from ..base_model import BaseModel
from ..required import REQUIRED


class OfferFlags(Enum):
    LSF_PASSIVE = 65536
    LSF_SELL = 131072


class OfferCreateFlags(Enum):
    TF_FILL_OR_KILL = 262144
    TF_IMMEDIATE_OR_CANCEL = 131072
    TF_PASSIVE = 65536
    TF_SELL = 524288


@dataclass(frozen=True)
class Offer(BaseModel):
    index: str = REQUIRED
    LedgerEntryType: LedgerEntryTypes = REQUIRED
    Flags: int = REQUIRED
    Account: str = REQUIRED
    Sequence: int = REQUIRED
    TakerPays: Amount = REQUIRED
    TakerGets: Amount = REQUIRED
    BookDirectory: str = REQUIRED
    BookNode: str = REQUIRED
    OwnerNode: str = REQUIRED
    PreviousTxnID: str = REQUIRED
    PreviousTxnLgrSeq: int = REQUIRED
    Expiration: Optional[XrplTimestamp] = None


@dataclass(frozen=True)
class BookOffer(Offer):
    #
    # Amount of the TakerGets currency the side placing the offer has available
    # to be traded. (XRP is represented as drops; any other currency is
    # represented as a decimal value.) If a trader has multiple offers in the
    # same book, only the highest-ranked offer includes this field.
    #
    owner_funds: Optional[str] = None
    #
    # The maximum amount of currency that the taker can get, given the funding
    # status of the offer.
    #
    taker_gets_funded: Optional[Amount] = None
    #
    # The maximum amount of currency that the taker would pay, given the funding
    # status of the offer.
    #
    taker_pays_funded: Optional[Amount] = None
    #
    # The exchange rate, as the ratio taker_pays divided by taker_gets. For
    # fairness, offers that have the same quality are automatically taken
    # first-in, first-out.
    #
    quality: Optional[str] = None
