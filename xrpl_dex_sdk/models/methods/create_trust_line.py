from dataclasses import dataclass
from typing import Any, Dict

from ..base_model import BaseModel
from ..required import REQUIRED
from ..common import CurrencyCode

#
# Expected response from a create_trust_line call
#
# @category Responses
#
@dataclass(frozen=True)
class CreateTrustLineResponse(BaseModel):
    code: CurrencyCode = REQUIRED
    amount: str = REQUIRED
    info: dict = REQUIRED
