from typing import NamedTuple, Optional


class Amount(NamedTuple):
    currency: str
    issuer: Optional[str]
    value: float
