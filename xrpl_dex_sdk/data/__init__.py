import json
import os
from typing import Any, Dict


def load_data(name: str) -> Dict:
    path = os.path.dirname(os.path.realpath(__file__)) + os.sep + name
    f = open(path, "r")
    data = f.read()
    f.close()
    return json.loads(data)


CurrenciesData: Dict[str, Dict[str, Any]] = load_data("currencies.json")
IssuersData: Dict[str, Dict[str, Any]] = load_data("issuers.json")
MarketsData: Dict[str, Dict[str, Any]] = load_data("markets.json")

__all__ = [
    "CurrenciesData",
    "IssuersData",
    "MarketsData",
]
