from dataclasses import dataclass, field
from typing import Any, Dict, Type, Union

from ...constants import ISO_CURRENCY_REGEX, HEX_CURRENCY_REGEX
from ..common import BigNumberish
from ..base_model import BaseModel
from ..required import REQUIRED


def is_valid_currency(candidate: str) -> bool:
    return bool(ISO_CURRENCY_REGEX.fullmatch(candidate) or HEX_CURRENCY_REGEX.fullmatch(candidate))


@dataclass(frozen=True)
class XRP(BaseModel):
    """
    Specifies XRP as a currency, without a value. Normally, you will not use this
    model as it does not specify an amount of XRP. In cases where you need to
    specify an amount of XRP, you will use a string. However, for some book order
    requests where currencies are specified without amounts, you may need to
    specify the use of XRP, without a value. In these cases, you will use this
    object.

    See https://xrpl.org/currency-formats.html#specifying-currency-amounts
    """

    currency: str = field(default="XRP", init=False)

    @classmethod
    def from_dict(cls: Type["XRP"], value: Dict[str, Any]) -> "XRP":
        """
        Construct a new XRP from a dictionary of parameters.

        Args:
            value: The value to construct the XRP from.

        Returns:
            A new XRP object, constructed using the given parameters.

        Raises:
            XRPLModelException: If the dictionary provided is invalid.
        """
        if len(value) != 1 or "currency" not in value or value["currency"] != "XRP":
            raise Exception("Not a valid XRP type")
        return XRP()

    def to_dict(self: "XRP") -> Dict[str, Any]:
        """
        Returns the dictionary representation of an XRP currency object.

        Returns:
            The dictionary representation of an XRP currency object.
        """
        return {**super().to_dict(), "currency": "XRP"}

    def to_amount(self: "XRP", value: Union[str, int]) -> str:
        """
        Converts value to XRP.

        Args:
            value: The amount of XRP.

        Returns:
            A string representation of XRP amount.
        """
        return str(value)


@dataclass(frozen=True)
class IssuedCurrency(BaseModel):
    """
    Specifies an amount in an issued currency, but without a value field.
    This format is used for some book order requests.

    See https://xrpl.org/currency-formats.html#specifying-currency-amounts
    """

    currency: str = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """

    issuer: str = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """

    def _get_errors(self: "IssuedCurrency") -> Dict[str, str]:
        errors = super()._get_errors()
        if self.currency.upper() == "XRP":
            errors["currency"] = "Currency must not be XRP for issued currency"
        elif not is_valid_currency(self.currency):
            errors["currency"] = f"Invalid currency {self.currency}"
        return errors

    def to_amount(self: "IssuedCurrency", value: BigNumberish) -> "IssuedCurrencyAmount":
        """
        Converts an IssuedCurrency to an IssuedCurrencyAmount.

        Args:
            value: The amount of issued currency in the IssuedCurrencyAmount.

        Returns:
            An IssuedCurrencyAmount that represents the issued currency and the
                provided value.
        """
        return IssuedCurrencyAmount(currency=self.currency, issuer=self.issuer, value=value)


@dataclass(frozen=True)
class IssuedCurrencyAmount(IssuedCurrency):
    """
    Specifies an amount in an issued currency.

    See https://xrpl.org/currency-formats.html#issued-currency-amounts.
    """

    value: BigNumberish = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """

    def to_currency(self: "IssuedCurrencyAmount") -> IssuedCurrency:
        """
        Build an IssuedCurrency from this IssuedCurrencyAmount.

        Returns:
            The IssuedCurrency for this IssuedCurrencyAmount.
        """
        return IssuedCurrency(issuer=self.issuer, currency=self.currency)

    def to_dict(self: "IssuedCurrencyAmount") -> Dict[str, str]:
        """
        Returns the dictionary representation of an IssuedCurrencyAmount.

        Returns:
            The dictionary representation of an IssuedCurrencyAmount.
        """
        return {**super().to_dict(), "value": str(self.value)}


Amount = Union[IssuedCurrencyAmount, str]
