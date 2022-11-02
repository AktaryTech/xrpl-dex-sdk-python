from dataclasses import dataclass
from typing import Any, List, Optional, Dict

from ..base_model import BaseModel
from ..required import REQUIRED
from ..ccxt.order import OrderId


@dataclass(frozen=True)
class CreateLimitBuyOrderParams(BaseModel):
    # Time after which the Offer is no longer active, in seconds since the Ripple Epoch. (1/1/2000) */
    expiration: Optional[int] = None
    # Additional arbitrary information used to identify this transaction */
    memos: Optional[List[Any]] = None
    # Order behavior (via XRPL OfferCreateFlags) */
    flags: Optional[int] = None


@dataclass(frozen=True)
class CreateLimitBuyOrderResponse(BaseModel):
    id: OrderId = REQUIRED
    info: dict = REQUIRED
