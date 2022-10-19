from dataclasses import dataclass
from typing import Dict, NamedTuple, Optional

from ...constants import CURRENCY_PRECISION
from ..common import CurrencyCode
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class Currency(BaseModel):
    code: CurrencyCode = REQUIRED
    fee: Optional[float] = None
    name: Optional[str] = None
    issuer_name: Optional[str] = None
    logo: Optional[str] = None
    precision: Optional[int] = CURRENCY_PRECISION


Currencies = Dict[CurrencyCode, Currency]

__all__ = ["Currency", "Currencies"]
