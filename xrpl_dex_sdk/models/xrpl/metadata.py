from dataclasses import dataclass
from typing import Any, Dict, Optional

from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class CreatedNode(BaseModel):
    LedgerEntryType: str = REQUIRED
    LedgerIndex: str = REQUIRED
    NewFields: Dict[str, Any] = REQUIRED


@dataclass(frozen=True)
class ModifiedNode(BaseModel):
    LedgerEntryType: str = REQUIRED
    LedgerIndex: str = REQUIRED
    FinalFields: Optional[Dict[str, Any]] = None
    PreviousFields: Optional[Dict[str, Any]] = None
    PreviousTxnID: Optional[str] = None
    PreviousTxnLgrSeq: Optional[int] = None


@dataclass(frozen=True)
class DeletedNode(BaseModel):
    LedgerEntryType: str = REQUIRED
    LedgerIndex: str = REQUIRED
    FinalFields: Dict[str, Any] = REQUIRED
    PreviousFields: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class Node(BaseModel):
    type: str = REQUIRED
    LedgerEntryType: str = REQUIRED
    LedgerIndex: str = REQUIRED
    NewFields: Optional[Dict[str, Any]] = None
    FinalFields: Optional[Dict[str, Any]] = None
    PreviousFields: Optional[Dict[str, Any]] = None
    PreviousTxnID: Optional[str] = None
    PreviousTxnLgrSeq: Optional[int] = None

    def _get_errors(self: "Node") -> Dict[str, str]:
        errors = super()._get_errors()
        if type == "CreatedNode":
            if self.NewFields == None:
                errors["node"] = "CreatedNode requires a NewFields property"
        elif type == "DeletedNode":
            if self.FinalFields == None:
                errors["node"] = "DeletedNode requires a FinalFields property"
        return errors
