from typing import Any, List, NamedTuple, Optional

from ..ccxt.orders import OrderId


class CreateLimitBuyOrderParams(NamedTuple):
    # Time after which the Offer is no longer active, in seconds since the Ripple Epoch. (1/1/2000) */
    expiration: Optional[int] = None
    # Additional arbitrary information used to identify this transaction */
    memos: Optional[List[Any]] = None
    # Order behavior (via XRPL OfferCreateFlags) */
    flags: Optional[int] = None


CreateLimitBuyOrderResponse = OrderId or None

__all__ = ["CreateLimitBuyOrderParams", "CreateLimitBuyOrderResponse"]
