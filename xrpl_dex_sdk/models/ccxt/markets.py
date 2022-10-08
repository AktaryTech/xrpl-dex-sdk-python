from typing import Any, Dict, List, NamedTuple, Optional

from ..common import CurrencyCode, MarketSymbol


class Market(NamedTuple):
    # String literal for referencing within an exchange
    id: str
    # Unified Market Symbol
    symbol: MarketSymbol
    # Base token
    base: CurrencyCode
    # Quote token
    quote: CurrencyCode
    # Base token transfer fee
    base_fee: float
    # Quote token transfer fee
    quote_fee: float
    # Whether transfer fees are percentages
    percentage: Optional[bool] = True


Markets = Dict[MarketSymbol, Market]

__all__ = ["Market", "Markets"]
