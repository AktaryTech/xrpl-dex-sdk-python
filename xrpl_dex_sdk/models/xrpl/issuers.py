from typing import Dict, List, NamedTuple

from ..common import CurrencyCode, AccountAddress


class IssuerCurrency(NamedTuple):
    code: CurrencyCode
    issuer: AccountAddress


class Issuer(NamedTuple):
    name: str
    trusted: bool
    website: str
    addresses: List[AccountAddress]
    currencies: List[CurrencyCode]
    transfer_rate: float


Issuers = Dict[str, Issuer]

__all__ = ["IssuerCurrency", "Issuer", "Issuers"]
