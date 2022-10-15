from typing import Any, Dict
from dateutil.parser import isoparse
from time import strptime, strftime
from xrpl.utils import ripple_time_to_posix, datetime_to_ripple_time

from ..constants import BILLION, SERVER_STATE_TIME_FORMAT
from ..models.common import CurrencyCode, MarketSymbol, IssuerAddress
from ..models.xrpl import Amount

# from ..models import Amount, IssuerAddress, CurrencyCode, MarketSymbol
from .orders import (
    get_base_amount_key,
    get_quote_amount_key,
    get_order_side_from_flags,
)


def transfer_rate_to_decimal(rate: int) -> float:
    if rate == 0:
        return float(0)
    decimal = (rate - BILLION) / BILLION
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


def server_time_to_posix(server_time: str) -> int:
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


#
# Gets a MarketSymbol from an Offer or Transaction.
# @param source The Offer or Transaction object to parse
# @returns
#
def get_market_symbol(source: Dict[str, Any]):
    side = get_order_side_from_flags(source["Flags"])
    return get_market_symbol_from_amount(
        source[get_base_amount_key(side)], source[get_quote_amount_key(side)]
    )


#
# * Gets a MarketSymbol from Base and Quote XRPL Amounts.
# * @param base Base currency as Amount object
# * @param quote Quote currency as Amount object
# * @returns
#
def get_market_symbol_from_amount(base: Amount, quote: Amount) -> MarketSymbol:
    base_code = (
        CurrencyCode("XRP")
        if isinstance(base, str)
        else CurrencyCode(base["currency"], base["issuer"])
    )
    quote_code = (
        CurrencyCode("XRP")
        if isinstance(quote, str)
        else CurrencyCode(quote["currency"], quote["issuer"])
    )
    return MarketSymbol(base_code.code, quote_code.code)


__all__ = [
    "transfer_rate_to_decimal",
    "decimal_to_transfer_rate",
    "server_time_to_posix",
    "get_market_symbol",
    "get_market_symbol_from_amount",
]
