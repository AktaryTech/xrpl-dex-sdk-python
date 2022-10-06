from typing import Any, Dict, NamedTuple

from ..common import CurrencyCode


class Balance(NamedTuple):
    free: float
    used: float
    total: float


class Balances(NamedTuple):
    balances: Dict[CurrencyCode, Balance]
    info: Dict[str, Any]
