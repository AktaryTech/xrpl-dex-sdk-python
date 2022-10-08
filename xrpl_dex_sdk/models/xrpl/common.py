from typing import Dict, Optional, Union

from ..common import CurrencyCode


class Amount:
    def __init__(self, currency: CurrencyCode, value: Optional[str] = None) -> None:
        self.currency = currency.code
        if currency.issuer != None:
            self.issuer = currency.issuer
        if value != None:
            self.value = value


# Amount = Union[Dict[str, str], str]

__all__ = ["Amount"]
