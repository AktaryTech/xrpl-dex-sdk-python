from typing import Dict, NamedTuple, Optional

from ...constants import CURRENCY_PRECISION
from ..common import CurrencyCode


class Currency(NamedTuple):
    code: CurrencyCode
    fee: Optional[float] = None
    name: Optional[str] = None
    issuer_name: Optional[str] = None
    logo: Optional[str] = None
    precision: Optional[int] = CURRENCY_PRECISION


Currencies = Dict[CurrencyCode, Currency]

__all__ = ["Currency", "Currencies"]
