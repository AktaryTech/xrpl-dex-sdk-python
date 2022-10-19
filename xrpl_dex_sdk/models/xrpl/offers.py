from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Optional, Union

from xrpl.models.amounts.issued_currency_amount import IssuedCurrencyAmount

from ..common import XrplTimestamp
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
    TakerPays: Union[str, IssuedCurrencyAmount] = REQUIRED
    TakerGets: Union[str, IssuedCurrencyAmount] = REQUIRED
    BookDirectory: str = REQUIRED
    BookNode: str = REQUIRED
    OwnerNode: str = REQUIRED
    PreviousTxnID: str = REQUIRED
    PreviousTxnLgrSeq: int = REQUIRED
    Expiration: Optional[XrplTimestamp] = None


__all__ = ["Offer", "OfferCreateFlags", "OfferFlags"]
