from math import floor

from ..constants import DROPS_PER_XRP


def drops_to_xrp(drops: int or str) -> float:
    return int(drops) / DROPS_PER_XRP


def xrp_to_drops(xrp: float) -> int:
    return floor(xrp * DROPS_PER_XRP)
