from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

from ..common import UnixTimestamp
from ..base_model import BaseModel
from ..required import REQUIRED


class ExchangeStatusType(Enum):
    """https://docs.ccxt.com/en/latest/manual.html?#exchange-status-structure"""

    OK = "ok"
    SHUTDOWN = "shutdown"
    ERROR = "error"
    MAINTENANCE = "maintenance"


@dataclass(frozen=True)
class ExchangeStatus(BaseModel):
    # Status is one of 'ok', 'shutdown', 'error', 'maintenance'
    status: ExchangeStatusType = REQUIRED
    # Raw response from exchange
    info: dict = REQUIRED
    # Integer, last updated timestamp in milliseconds if updated via the API
    updated: Optional[UnixTimestamp] = None
    # When the maintenance or outage is expected to end
    eta: Optional[UnixTimestamp] = None
    # A link to a GitHub issue or to an exchange post on the subject
    url: Optional[str] = None
