from dataclasses import dataclass
from typing import Any, Dict, Optional

from ..ccxt import Balances
from ..common import CurrencyCode
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class FetchBalanceParams(BaseModel):
    code: Optional[CurrencyCode] = None


@dataclass(frozen=True)
class FetchBalanceResponse(BaseModel):
    balances: Balances = REQUIRED
    info: dict = REQUIRED
