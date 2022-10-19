from dataclasses import dataclass
from typing import Any, Dict, Optional

from .base_model import BaseModel
from .required import REQUIRED
from ..constants import ISO_CURRENCY_REGEX, HEX_CURRENCY_REGEX

AccountAddress = str
IssuerAddress = AccountAddress


@dataclass(frozen=True)
class OrderId(BaseModel):
    account: AccountAddress = REQUIRED
    sequence: int = REQUIRED

    @classmethod
    def from_string(cls, id: str):
        try:
            [account, sequence] = id.split(":")
            return cls(account=account, sequence=sequence)
        except:
            raise Exception(f"Invalid OrderId: {id}")

    def to_id(self) -> str:
        return self.account + ":" + str(self.sequence)

    def __str__(self) -> str:
        return self.to_id()


@dataclass(frozen=True)
class TradeId(BaseModel):
    account: AccountAddress = REQUIRED
    sequence: int = REQUIRED

    @classmethod
    def from_string(cls, id: str):
        try:
            [account, sequence] = id.split(":")
            return cls(account=account, sequence=sequence)
        except:
            raise Exception(f"Invalid TradeId: {id}")

    def to_id(self) -> str:
        return self.account + ":" + str(self.sequence)

    def __str__(self) -> str:
        return self.to_id()


@dataclass(frozen=True)
class CurrencyCode(BaseModel):
    currency: str = REQUIRED
    issuer: Optional[str] = None

    @classmethod
    def from_string(cls, code: str):
        code_arr = code.split("+")
        if len(code_arr) < 1 or len(code_arr) > 2:
            raise Exception(f"Invalid currency code: {code}")
        currency = code_arr[0]
        issuer = code_arr[1] if len(code_arr) == 2 else None
        return cls(currency=currency, issuer=issuer)

    def to_code(self) -> str:
        return self.currency + ("+" + self.issuer if self.issuer != None else "")

    def is_xrp(self) -> bool:
        return self.currency.upper() == "XRP"

    def has_issuer(self) -> bool:
        return self.issuer != None

    def _get_errors(self: "CurrencyCode") -> Dict[str, str]:
        errors = super()._get_errors()
        if self.currency.upper() == "XRP" and self.issuer != None:
            errors["currency"] = "XRP does not require an Issuer"
        elif not self._is_valid_currency(self.currency):
            errors["currency"] = f"Invalid currency: {self.currency}"
        return errors

    def _is_valid_currency(self, value: str) -> bool:
        return bool(
            ISO_CURRENCY_REGEX.fullmatch(value) or HEX_CURRENCY_REGEX.fullmatch(value)
        )

    def __str__(self) -> str:
        return self.to_code()


@dataclass(frozen=True)
class MarketSymbol(BaseModel):
    base: CurrencyCode = REQUIRED
    quote: CurrencyCode = REQUIRED

    @classmethod
    def from_string(cls, symbol: str):
        symbol_arr = symbol.split("/")
        if len(symbol_arr) != 2:
            raise Exception(f"Invalid market symbol: {symbol}")
        base = CurrencyCode.from_string(symbol_arr[0])
        quote = CurrencyCode.from_string(symbol_arr[1])
        return cls(base=base, quote=quote)

    def to_symbol(self) -> str:
        return f"{str(self.base)}/{str(self.quote)}"

    def __str__(self) -> str:
        return self.to_symbol()


UnixTimestamp = int  # milliseconds since start of Unix epoch (1/1/1970)
UnixISOTimestamp = str  # ISO8601 datetime with milliseconds
XrplTimestamp = int  # milliseconds since start of XRPL epoch (1/1/2000)

__all__ = [
    "AccountAddress",
    "IssuerAddress",
    "OrderId",
    "TradeId",
    "CurrencyCode",
    "MarketSymbol",
    "UnixTimestamp",
    "UnixISOTimestamp",
    "XrplTimestamp",
]
