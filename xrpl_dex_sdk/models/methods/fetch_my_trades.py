from dataclasses import dataclass
from typing import Optional

from ..ccxt import Trades
from ...constants import DEFAULT_SEARCH_LIMIT
from ..base_model import BaseModel


@dataclass(frozen=True)
class FetchMyTradesParams(BaseModel):
    # Max items to search through looking for Trades before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


FetchMyTradesResponse = Trades
