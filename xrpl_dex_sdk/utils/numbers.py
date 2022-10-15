from typing import Dict, Union
from ..models.xrpl import Amount


def parse_amount_value(amount: Amount) -> Union[float, int]:
    return int(amount) if isinstance(amount, str) else float(amount["value"])


def subtract_amounts(amount: Amount, subtractor: Amount) -> Amount:
    amount_value = parse_amount_value(amount)
    subtractor_value = parse_amount_value(subtractor)
    result_value = amount_value - subtractor_value

    new_amount = amount
    if isinstance(new_amount, Dict):
        new_amount["value"] = str(result_value)
    else:
        new_amount = str(result_value)

    return new_amount


__all__ = ["parse_amount_value", "subtract_amounts"]
