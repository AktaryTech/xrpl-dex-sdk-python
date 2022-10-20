from typing import Any, Dict, List, NamedTuple, Optional

from .common import Amount
from .metadata import Node
from ..common import UnixTimestamp, XrplTimestamp
from ..xrpl import Offer


class TransactionMetadata(NamedTuple):
    AffectedNodes: List[Node]
    TransactionIndex: int
    TransactionResult: str
    DeliveredAmount: Optional[Amount]
    delivered_amount: Optional[Amount or str]


class Warning(NamedTuple):
    id: int
    message: str
    details: Dict[str, str]


class BaseTxResponse(NamedTuple):
    id: int or str
    status: Optional[str]
    type: str
    result: Any
    warning: Optional[str]
    warnings: Optional[List[Warning]]
    forwarded: Optional[bool]
    api_version: Optional[int]


class TxResult(NamedTuple):
    hash: str
    ledger_index: int
    meta: TransactionMetadata or str
    validated: bool
    date: XrplTimestamp


class TransactionData(NamedTuple):
    transaction: Any
    metadata: TransactionMetadata
    offers: List[Offer]
    previous_txn_id: Optional[str]
    date: UnixTimestamp


__all__ = [
    "TransactionMetadata",
    "Warning",
    "BaseTxResponse",
    "TxResult",
    "TransactionData",
]
