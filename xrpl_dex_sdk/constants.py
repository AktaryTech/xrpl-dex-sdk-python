import re
from enum import Enum
import os
from typing import Dict, Final, Pattern


DEFAULT_LIMIT: int = int(os.getenv("XRPL_DEFAULT_LIMIT", 20))
DEFAULT_SEARCH_LIMIT: int = int(os.getenv("XRPL_DEFAULT_SEARCH_LIMIT", 200))
DEFAULT_TICKER_SEARCH_LIMIT: int = int(os.getenv("XRPL_DEFAULT_TICKER_SEARCH_LIMIT", 100))


class NetworkNames(Enum):
    TESTNET = "TESTNET"
    DEVNET = "DEVNET"
    MAINNET = "MAINNET"
    LOCAL = "LOCAL"


TESTNET: str = "TESTNET"
DEVNET: str = "DEVNET"
MAINNET: str = "MAINNET"
LOCAL: str = "LOCAL"

MAINNET_URL: str = os.getenv("XRPL_MAINNET_URL", "s1.ripple.com")
MAINNET_FULL_HISTORY_1_URL: str = os.getenv("XRPL_MAINNET_FULL_HISTORY_1_URL", "xrplcluster.com")
MAINNET_FULL_HISTORY_2_URL: str = os.getenv("XRPL_MAINNET_FULL_HISTORY_2_URL", "s2.ripple.com")
TESTNET_URL: str = os.getenv("XRPL_TESTNET_URL", "s.altnet.rippletest.net")
DEVNET_URL: str = os.getenv("XRPL_DEVNET_URL", "s.devnet.rippletest.net")
NFT_DEVNET_URL: str = os.getenv("XRPL_NFT_DEVNET_URL", "xls20-sandbox.rippletest.net")
LOCAL_URL: str = os.getenv("XRPL_LOCAL_URL", "localhost:6006")

RPC_TESTNET: str = "https://" + TESTNET_URL + ":51234/"
RPC_DEVNET: str = "https://" + DEVNET_URL + ":51234/"
RPC_MAINNET: str = "https://" + MAINNET_URL + ":51234/"
RPC_LOCAL: str = "https://" + LOCAL_URL + "/"

WS_TESTNET: str = "wss://" + TESTNET_URL + ":51233/"
WS_DEVNET: str = "wss://" + DEVNET_URL + ":51233/"
WS_MAINNET: str = "wss://" + MAINNET_URL + "/"
WS_LOCAL: str = "wss://" + LOCAL_URL + "/"

CURRENCY_PRECISION: int = int(os.getenv("XRPL_CURRENCY_PRECISION", 15))
DROPS_PER_XRP: int = 1000000
FEE_CURRENCY: str = "XRP"
REFERENCE_TX_COST: int = 10
ACCOUNT_DELETE_TX_COST: int = 2000000
BILLION: int = 1000000000

Networks: Dict[str, Dict[str, str]] = {
    MAINNET: {
        "json_rpc": RPC_MAINNET,
        "ws": WS_MAINNET,
    },
    TESTNET: {
        "json_rpc": RPC_TESTNET,
        "ws": WS_TESTNET,
    },
    DEVNET: {
        "json_rpc": RPC_DEVNET,
        "ws": WS_DEVNET,
    },
    LOCAL: {"json_rpc": RPC_LOCAL, "ws": WS_LOCAL},
}

SERVER_STATE_TIME_FORMAT: str = "%Y-%b-%d %H:%M:%S.%f %Z"

ISO_CURRENCY_REGEX: Final[Pattern[str]] = re.compile("[A-Za-z0-9]{3}")
"""
Matches ISO currencies like "USD" or "EUR" in the format allowed by XRPL.

:meta private:
"""

HEX_CURRENCY_REGEX: Final[Pattern[str]] = re.compile("[A-F0-9]{40}")
"""
Matches hex-encoded currencies in the format allowed by XRPL.

:meta private:
"""

__all__ = [
    "DEFAULT_LIMIT",
    "NetworkNames",
    "TESTNET",
    "DEVNET",
    "MAINNET",
    "LOCAL",
    "MAINNET_URL",
    "MAINNET_FULL_HISTORY_1_URL",
    "MAINNET_FULL_HISTORY_2_URL",
    "TESTNET_URL",
    "DEVNET_URL",
    "NFT_DEVNET_URL",
    "LOCAL_URL",
    "RPC_TESTNET",
    "RPC_DEVNET",
    "RPC_MAINNET",
    "RPC_LOCAL",
    "WS_TESTNET",
    "WS_DEVNET",
    "WS_MAINNET",
    "WS_LOCAL",
    "CURRENCY_PRECISION",
    "DROPS_PER_XRP",
    "FEE_CURRENCY",
    "REFERENCE_TX_COST",
    "ACCOUNT_DELETE_TX_COST",
    "BILLION",
    "Networks",
    "SERVER_STATE_TIME_FORMAT",
    "ISO_CURRENCY_REGEX",
    "HEX_CURRENCY_REGEX",
]
