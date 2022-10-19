from dataclasses import dataclass
from typing import Callable, NamedTuple, Optional

from ..common import CurrencyCode
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class WatchBalanceParams(BaseModel):
    # Listener to send balance updates to
    listener: Callable = REQUIRED
    # Currency to fetch balances for
    code: Optional[CurrencyCode] = None


__all__ = ["WatchBalanceParams"]
