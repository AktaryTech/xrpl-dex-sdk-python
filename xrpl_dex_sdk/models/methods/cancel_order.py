from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from xrpl.models.transactions import Memo

from ..ccxt.order import OrderId
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class CancelOrderParams(BaseModel):
    account_txn_id: Optional[str] = None
    fee: Optional[str] = None
    flags: Optional[Union[Dict[str, bool], int, List[int]]] = 0
    last_ledger_sequence: Optional[int] = None
    memos: Optional[List[Memo]] = None
    sequence: Optional[int] = None
    source_tag: Optional[int] = None


@dataclass(frozen=True)
class CancelOrderResponse(BaseModel):
    id: OrderId = REQUIRED
    info: dict = REQUIRED
