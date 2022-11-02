from dataclasses import dataclass
from typing import Callable, Optional

from ...constants import DEFAULT_SEARCH_LIMIT
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class WatchOrderBookParams(BaseModel):
    # Listener to send balance updates to
    listener: Callable = REQUIRED
    # Max Transactions to search through looking for Order Book data before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT
