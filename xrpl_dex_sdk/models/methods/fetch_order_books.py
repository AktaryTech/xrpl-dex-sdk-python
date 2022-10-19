from dataclasses import dataclass
from typing import Dict, NamedTuple, Optional

from ..ccxt.order_book import OrderBooks
from ..common import MarketSymbol
from .fetch_order_book import FetchOrderBookParams
from ..base_model import BaseModel

#
# Request parameters for a fetch_order_book call
#
# @category Parameters
#
@dataclass(frozen=True)
class FetchOrderBooksParams(BaseModel):
    # Options for each symbol
    symbols: Optional[Dict[MarketSymbol, FetchOrderBookParams]] = None


#
# Expected response from a fetch_order_book call
#
# @category Responses
#
FetchOrderBooksResponse = OrderBooks

__all__ = ["FetchOrderBooksParams", "FetchOrderBooksResponse"]
