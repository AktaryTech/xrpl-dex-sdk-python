from typing import Any, Dict, List, NamedTuple, Optional

from ..common import CurrencyCode, MarketSymbol


class Fee(NamedTuple):
    # Fee currency
    currency: CurrencyCode
    # The fee cost (base_fee # rate)
    cost: float
    # The fee rate, 0.05% = 0.0005, 1% = 0.01, ...
    rate: Optional[float] = None
    # Whether the fee rate is a percentage or flat rate
    percentage: Optional[bool] = True


#
# This is returned by `fetchTransactionFee(s)`
#
class TransactionFee(NamedTuple):
    # The currency being transacted #
    code: CurrencyCode
    # The current cost in drops of XRP to send a transaction #
    current: int
    # The transfer fee (if any) for the given issuers #
    transfer: float
    # Raw response from exchange
    info: Dict[str, Any]


#
# This is returned by `fetchTradingFee(s)`
#
class TradingFee(NamedTuple):
    # Unified Market Symbol #
    symbol: MarketSymbol
    # Fee rate for base token #
    base: float
    # Fee rate for quote token #
    quote: float
    # Raw response from exchange
    info: Dict[str, Any]
    # Whether the fees are a percentage or flat rate #
    percentage: Optional[bool] = True


#
# This is returned by `fetchFees`
#
class FeeSchedule(NamedTuple):
    transactions: List[TransactionFee]
    trading: List[TradingFee]


__all__ = ["Fee", "TransactionFee", "TradingFee", "FeeSchedule"]
