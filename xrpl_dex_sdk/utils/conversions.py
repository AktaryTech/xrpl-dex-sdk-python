from ..constants import BILLION


def transfer_rate_to_decimal(rate: int) -> float:
    if rate == 0:
        return 0
    decimal = rate - BILLION / BILLION
    if decimal < 0:
        return
    return decimal


def decimal_to_transfer_rate(decimal: float) -> int:
    rate = decimal * BILLION + BILLION
    if rate < BILLION or rate > (BILLION * 2):
        return
    if rate == BILLION:
        return 0
    return rate
