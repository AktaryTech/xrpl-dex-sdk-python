from typing import Dict, Optional

from ..common import CurrencyCode, MarketSymbol


class Market:
    # String literal for referencing within an exchange
    id: str
    # Unified Market Symbol
    symbol: MarketSymbol
    # Base token
    base: CurrencyCode
    # Quote token
    quote: CurrencyCode
    # Base token transfer fee
    base_fee: float = 0
    # Quote token transfer fee
    quote_fee: float = 0
    # Whether transfer fees are percentages
    percentage: Optional[bool] = True


Markets = Dict[MarketSymbol, Market]

__all__ = ["Market", "Markets"]
