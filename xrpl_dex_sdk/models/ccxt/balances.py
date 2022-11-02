from dataclasses import dataclass
from typing import Dict

from ..common import CurrencyCode
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class Balance(BaseModel):
    """https://docs.ccxt.com/en/latest/manual.html?#balance-structure"""

    free: float = REQUIRED
    used: float = REQUIRED
    total: float = REQUIRED


Balances = Dict[CurrencyCode, Balance]
