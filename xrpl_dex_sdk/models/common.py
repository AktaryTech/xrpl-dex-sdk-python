from typing import Optional


AccountAddress = str
IssuerAddress = AccountAddress


class CurrencyCode:
    def __init__(self, currency: str, issuer: Optional[IssuerAddress] = None) -> None:
        self.currency = currency
        self.issuer = issuer
        self.code = currency + "+" + issuer if issuer != None else currency

    def __repr__(self) -> str:
        return self.code

    def __str__(self) -> str:
        return self.code


class MarketSymbol:
    def __init__(self, base: CurrencyCode, quote: CurrencyCode) -> None:
        self.base = base
        self.quote = quote
        self.symbol = base.code + "/" + quote.code

    def __repr__(self) -> str:
        return self.symbol

    def __str__(self) -> str:
        return self.symbol


UnixTimestamp = int  # milliseconds since start of Unix epoch (1/1/1970)
UnixISOTimestamp = str  # ISO8601 datetime with milliseconds
XrplTimestamp = int  # milliseconds since start of XRPL epoch (1/1/2000)

__all__ = [
    "AccountAddress",
    "IssuerAddress",
    "CurrencyCode",
    "MarketSymbol",
    "UnixTimestamp",
    "UnixISOTimestamp",
    "XrplTimestamp",
]
