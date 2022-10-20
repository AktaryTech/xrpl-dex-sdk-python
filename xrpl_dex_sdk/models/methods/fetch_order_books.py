from typing import Dict, NamedTuple, Optional

from ..ccxt.order_book import OrderBooks
from ..common import MarketSymbol
from .fetch_order_book import FetchOrderBookParams

#
# Request parameters for a fetch_order_book call
#
# @category Parameters
#
class FetchOrderBooksParams(NamedTuple):
    # Options for each symbol
    symbols: Dict[MarketSymbol, FetchOrderBookParams] = {}


#
# Expected response from a fetch_order_book call
#
# @category Responses
#
FetchOrderBooksResponse = OrderBooks

__all__ = ["FetchOrderBooksParams", "FetchOrderBooksResponse"]
