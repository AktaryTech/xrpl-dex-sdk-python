from dataclasses import dataclass
from typing import Callable, Optional

from ...constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class WatchOrdersParams(BaseModel):
    # Listener to send balance updates to
    listener: Callable = REQUIRED
    # Number of results to return
    limit: Optional[int] = DEFAULT_LIMIT
    # Max Transactions to search through looking for Order data before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT
    # Whether to return Open orders
    show_open: Optional[bool] = True
    # Whether to return Closed orders
    show_closed: Optional[bool] = True
    # Whether to return Canceled orders
    show_canceled: Optional[bool] = True
