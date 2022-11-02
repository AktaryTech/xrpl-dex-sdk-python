from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from .currency import Amount
from .metadata import Node
from ..common import UnixTimestamp, XrplTimestamp
from ..xrpl import Offer
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class TransactionMetadata(BaseModel):
    AffectedNodes: List[Node] = REQUIRED
    TransactionIndex: int = REQUIRED
    TransactionResult: str = REQUIRED
    DeliveredAmount: Optional[Amount] = None
    delivered_amount: Optional[Union[Amount, str]] = None


@dataclass(frozen=True)
class Warning(BaseModel):
    id: int = REQUIRED
    message: str = REQUIRED
    details: Dict[str, str] = REQUIRED


@dataclass(frozen=True)
class BaseTxResponse(BaseModel):
    id: Union[int, str] = REQUIRED
    status: Optional[str] = None
    type: str = REQUIRED
    result: Any = REQUIRED
    warning: Optional[str] = None
    warnings: Optional[List[Warning]] = None
    forwarded: Optional[bool] = None
    api_version: Optional[int] = None


@dataclass(frozen=True)
class TxResult(BaseModel):
    hash: str = REQUIRED
    ledger_index: int = REQUIRED
    meta: Union[TransactionMetadata, str] = REQUIRED
    validated: bool = REQUIRED
    date: XrplTimestamp = REQUIRED


@dataclass(frozen=True)
class TransactionData(BaseModel):
    transaction: Any = REQUIRED
    metadata: TransactionMetadata = REQUIRED
    offers: List[Offer] = REQUIRED
    previous_txn_id: Optional[str] = None
    date: UnixTimestamp = REQUIRED
