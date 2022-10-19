"""_top-level exports for the data package."""
import json
import os
from typing import Any, Dict

from ..models.ccxt.currencies import Currencies
from ..models.xrpl.issuers import Issuers
from ..models.ccxt.markets import Markets
from .currencies import CurrenciesData
from .issuers import IssuersData
from .markets import MarketsData


def load_data(name: str) -> Dict:
    path = os.path.dirname(os.path.realpath(__file__)) + os.sep + name
    f = open(path, "r")
    data = f.read()
    f.close()
    return json.loads(data)


currencies_data: Dict[str, Dict[str, Any]] = load_data("currencies.json")
issuers_data: Dict[str, Dict[str, Any]] = load_data("issuers.json")
markets_data: Dict[str, Dict[str, Any]] = load_data("markets.json")

__all__ = [
    "CurrenciesData",
    "IssuersData",
    "MarketsData",
    "currencies_data",
    "issuers_data",
    "markets_data",
]
