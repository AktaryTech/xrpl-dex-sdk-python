from dataclasses import dataclass
from typing import Dict, Optional

from ...constants import CURRENCY_PRECISION
from ..common import CurrencyCode
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class Currency(BaseModel):
    """https://docs.ccxt.com/en/latest/manual.html?#currency-structure"""

    code: CurrencyCode = REQUIRED
    fee: Optional[float] = None
    name: Optional[str] = None
    issuer_name: Optional[str] = None
    logo: Optional[str] = None
    precision: Optional[int] = CURRENCY_PRECISION


Currencies = Dict[CurrencyCode, Currency]
