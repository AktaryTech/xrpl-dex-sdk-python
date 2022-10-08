from typing import Any, Dict, List, NamedTuple, Optional, Union
from ..ccxt.orders import OrderId

from xrpl.models.transactions import Memo


class CancelOrderParams(NamedTuple):
    account_txn_id: Optional[str] = None
    fee: Optional[str] = None
    flags: Union[Dict[str, bool], int, List[int]] = 0
    last_ledger_sequence: Optional[int] = None
    memos: Optional[List[Memo]] = None
    sequence: Optional[int] = None
    source_tag: Optional[int] = None


class CancelOrderResponse(NamedTuple):
    id: OrderId
    info: Dict[str, Any]


__all__ = ["CancelOrderParams", "CancelOrderResponse"]
