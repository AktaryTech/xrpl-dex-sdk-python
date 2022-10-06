from typing import Any, Dict, List, NamedTuple, Optional

from .amounts import Amount
from ..common import XrplTimestamp


class _CreatedNode(NamedTuple):
    LedgerEntryType: str
    LedgerIndex: str
    NewFields: Dict[str, Any]


CreatedNode = Dict["CreatedNode", _CreatedNode]


class _ModifiedNode(NamedTuple):
    LedgerEntryType: str
    LedgerIndex: str
    FinalFields: Optional[Dict[str, Any]]
    PreviousFields: Optional[Dict[str, Any]]
    PreviousTxnID: Optional[str]
    PreviouTxnLgrSeq: Optional[int]


ModifiedNode = Dict["ModifiedNode", _ModifiedNode]


class _DeletedNode(NamedTuple):
    LedgerEntryType: str
    LedgerIndex: str
    FinalFields: Dict[str, Any]
    PreviousFields: Optional[Dict[str, Any]]


DeletedNode = Dict["DeletedNode", _DeletedNode]

Node = CreatedNode or ModifiedNode or DeletedNode


class TransactionMetadata(NamedTuple):
    AffectedNodes: List[Node]
    DeliveredAmount: Optional[Amount]
    delivered_amount: Optional[Amount or str]
    TransactionIndex: int
    TransactionResult: str


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


# class TxResponse(NamedTuple):
#   result:{
#     hash: str,
#     ledger_index: int,
#     meta: TransactionMetadata or str,
#     validated: boolean,
#     date: int,
#   },
#   searched_all: boolean

__all__ = [
    "CreatedNode",
    "ModifiedNode",
    "DeletedNode",
    "Node",
    "TransactionMetadata",
    "Warning",
    "BaseTxResponse",
    "TxResult",
]
