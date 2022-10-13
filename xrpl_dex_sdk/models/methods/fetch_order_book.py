from typing import NamedTuple, Optional, Union

from ..ccxt.order_book import OrderBook
from ..common import AccountAddress
from ...constants import DEFAULT_SEARCH_LIMIT

#
# Request parameters for a fetch_order_book call
#
# @category Parameters
#
class FetchOrderBookParams(NamedTuple):
    # Max Orders to search through while gathering Order Book data
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT
    # Get order book from the given ledger
    ledger_index: Optional[Union[str, int]] = None
    # Get order book from the provided hash
    ledger_hash: Optional[str] = None
    # Perspective from which to search for offers
    taker: Optional[AccountAddress] = None


#
# Expected response from a fetch_order_book call
#
# @category Responses
#
FetchOrderBookResponse = OrderBook

__all__ = ["FetchOrderBookParams", "FetchOrderBookResponse"]