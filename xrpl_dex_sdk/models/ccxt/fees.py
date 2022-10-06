from typing import NamedTuple, Optional

from ..common import CurrencyCode


class Fee(NamedTuple):
    # Fee currency
    currency: CurrencyCode
    # The fee cost (base_fee * rate)
    cost: float
    # The fee rate, 0.05% = 0.0005, 1% = 0.01, ...
    rate: Optional[float]
    # Whether the fee rate is a percentage or flat rate
    percentage: bool
