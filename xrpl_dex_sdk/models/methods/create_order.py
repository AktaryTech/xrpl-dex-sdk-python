from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from xrpl.models.transactions import Memo

from ..base_model import BaseModel
from ..required import REQUIRED
from ..ccxt.order import OrderId


@dataclass(frozen=True)
class CreateOrderParams(BaseModel):
    # Time after which the Offer is no longer active, in seconds since the Ripple Epoch. (1/1/2000) */
    expiration: Optional[int] = None
    account_txn_id: Optional[str] = None
    fee: Optional[str] = None
    # Order behavior (via XRPL OfferCreateFlags) */
    flags: Optional[Dict[str, bool]] = None
    last_ledger_sequence: Optional[int] = None
    # Additional arbitrary information used to identify this transaction */
    memos: Optional[List[Memo]] = None
    offer_sequence: Optional[int] = None
    sequence: Optional[int] = None
    source_tag: Optional[int] = None


@dataclass(frozen=True)
class CreateOrderResponse(BaseModel):
    id: OrderId = REQUIRED
    info: dict = REQUIRED
