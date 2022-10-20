from typing import Any, Dict, List, NamedTuple, Optional, Union

from xrpl.models.transactions import Memo

from ..ccxt.orders import OrderId


class CreateOrderParams(NamedTuple):
    # Time after which the Offer is no longer active, in seconds since the Ripple Epoch. (1/1/2000) */
    expiration: Optional[int] = None
    account_txn_id: Optional[str] = None
    fee: Optional[str] = None
    # Order behavior (via XRPL OfferCreateFlags) */
    flags: Dict[str, bool] = None
    last_ledger_sequence: Optional[int] = None
    # Additional arbitrary information used to identify this transaction */
    memos: Optional[List[Memo]] = None
    offer_sequence: Optional[int] = None
    sequence: Optional[int] = None
    source_tag: Optional[int] = None


class CreateOrderResponse(NamedTuple):
    id: OrderId
    info: Dict[str, Any]


__all__ = ["CreateOrderParams", "CreateOrderResponse"]
