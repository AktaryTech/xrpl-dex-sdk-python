from dataclasses import dataclass
from typing import Dict, Optional, Union

from ..common import CurrencyCode
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class IssuedCurrencyAmount(BaseModel):
    currency: str = REQUIRED
    issuer: Optional[str] = None
    value: Optional[str] = None


Amount = Union[IssuedCurrencyAmount, str]

__all__ = ["Amount", "IssuedCurrencyAmount"]
