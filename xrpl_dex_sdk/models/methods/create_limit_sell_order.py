from typing import Any, List, NamedTuple, Optional

from ..ccxt.orders import OrderId


class CreateLimitSellOrderParams(NamedTuple):
    # Time after which the Offer is no longer active, in seconds since the Ripple Epoch. (1/1/2000) */
    expiration: Optional[int] = None
    # Additional arbitrary information used to identify this transaction */
    memos: List[Any] = []
    # Order behavior (via XRPL OfferCreateFlags) */
    flags: Optional[int] = None


CreateLimitSellOrderResponse = OrderId or None

__all__ = ["CreateLimitSellOrderParams", "CreateLimitSellOrderResponse"]
