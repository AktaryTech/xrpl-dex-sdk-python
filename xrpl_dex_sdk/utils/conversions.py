from typing import Optional
from dateutil.parser import isoparse
from time import strptime, strftime
from xrpl.utils import ripple_time_to_posix, datetime_to_ripple_time

from ..constants import BILLION, SERVER_STATE_TIME_FORMAT


def transfer_rate_to_decimal(rate: int) -> Optional[float]:
    """Converts an XRPL transfer rate from percentage to decimal."""

    if rate == 0:
        return float(0)
    decimal = (rate - BILLION) / BILLION
    if decimal < 0:
        return
    return decimal


def decimal_to_transfer_rate(decimal: float) -> Optional[float]:
    """Converts a decimal to an XRPL transfer rate percentage."""

    rate = decimal * BILLION + BILLION
    if rate < BILLION or rate > (BILLION * 2):
        return
    if rate == BILLION:
        return 0
    return rate


def server_time_to_posix(server_time: str) -> int:
    """Parses XRPL server_status response and returns as POSIX timestamp."""

    microseconds = server_time.split(".")[1][:3]
    posix_time = ripple_time_to_posix(
        datetime_to_ripple_time(
            isoparse(
                strftime(
                    "%Y-%m-%dT%H:%M:%SZ",
                    strptime(server_time, SERVER_STATE_TIME_FORMAT),
                )
            )
        )
    )
    return int(str(posix_time) + str(microseconds))
