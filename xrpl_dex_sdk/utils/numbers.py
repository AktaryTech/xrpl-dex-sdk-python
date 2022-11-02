from typing import Union

from ..models.xrpl import Amount


def parse_amount_value(amount: Amount) -> Union[float, int]:
    """Parses an Amount object and returns the value as a number."""

    return (
        int(amount)
        if isinstance(amount, str)
        else float(amount["value"] if isinstance(amount, dict) else amount.value)
    )


def subtract_amounts(amount: Amount, subtractor: Amount) -> Amount:
    """Subtracts one Amount from another, and returns the difference as an Amount."""

    amount_value = parse_amount_value(amount)
    subtractor_value = parse_amount_value(subtractor)
    result_value = amount_value - subtractor_value

    new_amount = amount
    if isinstance(new_amount, dict):
        new_amount["value"] = str(result_value)
    else:
        new_amount = str(result_value)

    return new_amount
