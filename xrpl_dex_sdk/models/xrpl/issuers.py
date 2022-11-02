from dataclasses import dataclass
from typing import Dict, List, Optional

from ..common import CurrencyCode, AccountAddress
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class Issuer(BaseModel):
    name: str = REQUIRED
    trusted: bool = REQUIRED
    website: Optional[str] = None
    addresses: List[AccountAddress] = REQUIRED
    currencies: List[CurrencyCode] = REQUIRED
    transfer_rate: Optional[float] = 0


Issuers = Dict[str, Issuer]
