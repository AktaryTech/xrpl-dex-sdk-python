from enum import Enum
from typing import Any, Dict, NamedTuple, Optional

from ...constants import CURRENCY_PRECISION
from ..common import CurrencyCode, UnixTimestamp


class ExchangeStatusType(Enum):
    OK = "ok"
    SHUTDOWN = "shutdown"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class ExchangeStatus(NamedTuple):
    # Status is one of 'ok', 'shutdown', 'error', 'maintenance'
    status: ExchangeStatusType
    # Raw response from exchange
    info: Dict[str, Any]
    # Integer, last updated timestamp in milliseconds if updated via the API
    updated: Optional[UnixTimestamp] = None
    # When the maintenance or outage is expected to end
    eta: Optional[UnixTimestamp] = None
    # A link to a GitHub issue or to an exchange post on the subject
    url: Optional[str] = None


__all__ = ["ExchangeStatusType", "ExchangeStatus"]
