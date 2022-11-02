from dataclasses import dataclass
from typing import Optional

from ...models.ccxt import Trades
from ...constants import DEFAULT_SEARCH_LIMIT
from ..base_model import BaseModel


@dataclass(frozen=True)
class FetchTradesParams(BaseModel):
    # Max items to search through looking for an Trades before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


FetchTradesResponse = Trades
