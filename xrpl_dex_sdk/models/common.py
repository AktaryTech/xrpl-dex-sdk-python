from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from .base_model import BaseModel
from .required import REQUIRED
from ..constants import ISO_CURRENCY_REGEX, HEX_CURRENCY_REGEX


# type aliases
AccountAddress = str
IssuerAddress = AccountAddress

BigNumberish = Union[str, int, float]

NetworkName = str

UnixTimestamp = int  # milliseconds since start of Unix epoch (1/1/1970)
UnixISOTimestamp = str  # ISO8601 datetime with milliseconds
XrplTimestamp = int  # milliseconds since start of XRPL epoch (1/1/2000)


@dataclass(frozen=True)
class OrderId(BaseModel):
    """
    Represents the ID of an Order made on the exchange.

    Attributes
    ----------
    account : AccountAddress
        Address of the Wallet that placed this Order.
    sequence : int
        Sequence number of the XRPL Offer behind the Order.
    """

    account: AccountAddress = REQUIRED
    sequence: int = REQUIRED

    @classmethod
    def from_string(cls, id: str):
        """Create a new OrderId from a given string."""
        try:
            [account, sequence] = id.split(":")
            return cls(account=account, sequence=int(sequence))
        except:
            raise Exception(f"Invalid OrderId: {id}")

    def to_id(self) -> str:
        """Return the OrderId as a string."""
        return self.account + ":" + str(self.sequence)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, dict) and "Account" in other and "Sequence" in other:
            return self.account == other["Account"] and self.sequence == other["Sequence"]
        elif isinstance(other, OrderId):
            return self.to_id() == other.to_id()
        elif isinstance(other, str):
            return self.to_id() == OrderId.from_string(other).to_id()
        else:
            return super().__eq__(other)

    def __str__(self) -> str:
        return self.to_id()


@dataclass(frozen=True)
class TradeId(BaseModel):
    """
    Represents the ID of a Trade made on the exchange.

    Attributes
    ----------
    account : AccountAddress
        Address of the Wallet that made this Trade.
    sequence : int
        Sequence number of the XRPL Offer behind the Trade.
    """

    account: AccountAddress = REQUIRED
    sequence: int = REQUIRED

    @classmethod
    def from_string(cls, id: str):
        """Create a new TradeId from a given string."""
        try:
            [account, sequence] = id.split(":")
            return cls(account=account, sequence=int(sequence))
        except:
            raise Exception(f"Invalid TradeId: {id}")

    def to_id(self) -> str:
        """Return the TradeId as a string."""
        return self.account + ":" + str(self.sequence)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, dict) and "Account" in other and "Sequence" in other:
            return self.account == other["Account"] and self.sequence == other["Sequence"]
        else:
            return super().__eq__(other)

    def __str__(self) -> str:
        return self.to_id()


@dataclass(frozen=True)
class CurrencyCode(BaseModel):
    """
    Represents a currency being traded on the exchange.

    Attributes
    ----------
    currency : str
        The currency code. Usually three uppercase letters or a hash string.
    issuer : Optional[IssuerAddress]
        Address of the currency's issuer. Leave blank if the currency is XRP.
    """

    currency: str = REQUIRED
    issuer: Optional[IssuerAddress] = None

    @classmethod
    def from_string(cls, code: str):
        """Create a new CurrencyCode instance from a given string."""
        code_arr = code.split("+")
        if len(code_arr) < 1 or len(code_arr) > 2:
            raise Exception(f"Invalid currency code: {code}")
        currency = code_arr[0]
        issuer = code_arr[1] if len(code_arr) == 2 else None
        return cls(currency=currency, issuer=issuer)

    def to_code(self) -> str:
        """Return the CurrencyCode as a string."""
        return self.currency + ("+" + self.issuer if self.issuer != None else "")

    def is_xrp(self) -> bool:
        """Returns true if this currency is XRP."""
        return self.currency.upper() == "XRP"

    def has_issuer(self) -> bool:
        """Returns true if this is an issued currency."""
        return self.issuer != None

    def _get_errors(self: "CurrencyCode") -> Dict[str, str]:
        errors = super()._get_errors()
        if self.currency.upper() == "XRP" and self.issuer != None:
            errors["currency"] = "XRP does not require an Issuer"
        elif not self._is_valid_currency(self.currency):
            errors["currency"] = f"Invalid currency: {self.currency}"
        return errors

    def _is_valid_currency(self, value: str) -> bool:
        return bool(ISO_CURRENCY_REGEX.fullmatch(value) or HEX_CURRENCY_REGEX.fullmatch(value))

    def __str__(self) -> str:
        return self.to_code()


@dataclass(frozen=True)
class MarketSymbol(BaseModel):
    """
    Represents a market pair on the exchange.

    Attributes
    ----------
    base : CurrencyCode
        The market pair's base currency.
    quote : CurrencyCode
        The market pair's quote currency.
    """

    base: CurrencyCode = REQUIRED
    quote: CurrencyCode = REQUIRED

    @classmethod
    def from_string(cls, symbol: str):
        """Create a new MarketSymbol instance from a given string."""
        symbol_arr = symbol.split("/")
        if len(symbol_arr) != 2:
            raise Exception(f"Invalid market symbol: {symbol}")
        base = CurrencyCode.from_string(symbol_arr[0])
        quote = CurrencyCode.from_string(symbol_arr[1])
        return cls(base=base, quote=quote)

    def to_symbol(self) -> str:
        """Return the MarketSymbol as a string."""
        return f"{str(self.base)}/{str(self.quote)}"

    def __str__(self) -> str:
        return self.to_symbol()
