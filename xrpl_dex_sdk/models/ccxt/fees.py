from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..common import CurrencyCode, MarketSymbol
from ..base_model import BaseModel
from ..required import REQUIRED


@dataclass(frozen=True)
class Fee(BaseModel):
    # Fee currency
    currency: CurrencyCode = REQUIRED
    # The fee cost (base_fee * rate)
    cost: float = REQUIRED
    # The fee rate, 0.05% = 0.0005, 1% = 0.01, ...
    rate: Optional[float] = None
    # Whether the fee rate is a percentage or flat rate
    percentage: Optional[bool] = True


#
# This is returned by `fetchTransactionFee(s)`
#
@dataclass(frozen=True)
class TransactionFee(BaseModel):
    """https://docs.ccxt.com/en/latest/manual.html?#fees"""

    # The currency being transacted #
    code: CurrencyCode = REQUIRED
    # The current cost in drops of XRP to send a transaction #
    current: int = REQUIRED
    # The transfer fee (if any) for the given issuers #
    transfer: Optional[float] = None
    # Raw response from exchange
    info: dict = REQUIRED


#
# This is returned by `fetchTradingFee(s)`
#
@dataclass(frozen=True)
class TradingFee(BaseModel):
    """https://docs.ccxt.com/en/latest/manual.html?#fees"""

    # Unified Market Symbol #
    symbol: MarketSymbol = REQUIRED
    # Fee rate for base token #
    base: float = REQUIRED
    # Fee rate for quote token #
    quote: float = REQUIRED
    # Raw response from exchange
    info: dict = REQUIRED
    # Whether the fees are a percentage or flat rate #
    percentage: Optional[bool] = True


#
# This is returned by `fetchFees`
#
@dataclass(frozen=True)
class FeeSchedule(BaseModel):
    """https://docs.ccxt.com/en/latest/manual.html?#fees"""

    transactions: List[TransactionFee] = REQUIRED
    trading: List[TradingFee] = REQUIRED
