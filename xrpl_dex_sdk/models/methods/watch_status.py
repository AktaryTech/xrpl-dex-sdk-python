from dataclasses import dataclass
from typing import Callable, NamedTuple
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class WatchStatusParams(BaseModel):
    # Listener to send balance updates to
    listener: Callable = REQUIRED
