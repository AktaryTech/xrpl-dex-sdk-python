from typing import Any, Dict, NamedTuple, Optional, Union


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

Node = Union[CreatedNode, ModifiedNode, DeletedNode]

__all__ = ["CreatedNode", "ModifiedNode", "DeletedNode", "Node"]
