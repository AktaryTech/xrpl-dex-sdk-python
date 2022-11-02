from dataclasses import dataclass
from typing import Dict, Optional

from ..common import CurrencyCode, MarketSymbol
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class Market(BaseModel):
    """https://docs.ccxt.com/en/latest/manual.html?#market-structure"""

    # String literal for referencing within an exchange
    id: str = REQUIRED
    # Unified Market Symbol
    symbol: MarketSymbol = REQUIRED
    # Base token
    base: CurrencyCode = REQUIRED
    # Quote token
    quote: CurrencyCode = REQUIRED
    # Base token transfer fee
    base_fee: Optional[float] = float(0)
    # Quote token transfer fee
    quote_fee: Optional[float] = float(0)
    # Whether transfer fees are percentages
    percentage: Optional[bool] = True


Markets = Dict[MarketSymbol, Market]
