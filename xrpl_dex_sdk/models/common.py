from typing import Optional, Union

from .common import MarketSymbol


AccountAddress = str
IssuerAddress = AccountAddress


class CurrencyCode:
    def __init__(self, code: str, issuer: Optional[str] = None) -> None:
        if isinstance(code, str) == False:
            raise Exception(
                "Error creating CurrencyCode: provided value is not a string"
            )
        currency_issuer_pair = [code, issuer] if issuer != None else code.split("+")
        if currency_issuer_pair[0] == None:
            raise Exception(
                "Error creating CurrencyCode: " + code + " is not a valid code"
            )
        self.currency = currency_issuer_pair[0]
        self.issuer = (
            currency_issuer_pair[1] if len(currency_issuer_pair) == 2 else None
        )
        self.code = self.currency
        if self.issuer != None:
            self.code += "+" + self.issuer

    def __repr__(self) -> str:
        return self.code

    def __str__(self) -> str:
        return self.code


class MarketSymbol:
    def __init__(self, symbol: str, quote_symbol: Optional[str] = None) -> None:
        if isinstance(symbol, str) == False:
            raise Exception(
                "Error creating MarketSymbol: provided value is not a string"
            )

        base_quote_pair = (
            [symbol, quote_symbol] if quote_symbol != None else symbol.split("/")
        )
        if (
            len(base_quote_pair) == 1
            or base_quote_pair[0] == None
            or base_quote_pair[1] == None
        ):
            raise Exception(
                "Error creating MarketSymbol: " + symbol + " is not a valid symbol"
            )
        self.base = CurrencyCode(base_quote_pair[0])
        self.quote = CurrencyCode(base_quote_pair[1])
        self.symbol = base_quote_pair[0] + "/" + base_quote_pair[1]

    def __repr__(self) -> str:
        return self.symbol

    def __str__(self) -> str:
        return self.symbol

    def __eq__(self, other_symbol: Optional[Union[MarketSymbol, str]]) -> bool:
        if other_symbol == None:
            return False
        other_symbol = (
            MarketSymbol(other_symbol)
            if isinstance(other_symbol, str)
            else other_symbol
        )
        return self.symbol == other_symbol.symbol


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
