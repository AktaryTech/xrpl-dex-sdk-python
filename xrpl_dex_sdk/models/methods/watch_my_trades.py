from dataclasses import dataclass
from typing import Callable, NamedTuple, Optional

from ...constants import DEFAULT_SEARCH_LIMIT
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class WatchMyTradesParams(BaseModel):
    # Listener to send balance updates to
    listener: Callable = REQUIRED
    # Max items to search through looking for Trades before giving up
    search_limit: Optional[int] = DEFAULT_SEARCH_LIMIT


__all__ = ["WatchMyTradesParams"]
