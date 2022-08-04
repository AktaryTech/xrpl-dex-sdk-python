import datetime
import json
import os
from typing import Any, Dict

import requests

# import websockets

__version__ = "0.1.0"

# const
LIMIT = int(os.getenv("RIPPLE_DEFAULT_LIMIT", 20))

TESTNET = os.getenv("RIPPLE_TESTNET_URL", "s.altnet.rippletest.net")
DEVNET = os.getenv("RIPPLE_DEVNET_URL", "s.devnet.rippletest.net")
MAINNET = os.getenv("RIPPLE_MAINNET_URL", "s1.ripple.com")

RPC_TESTNET = "https://" + TESTNET + ":51234/"
RPC_DEVNET = "https://" + DEVNET + ":51234/"
RPC_MAINNET = "https://" + MAINNET + ":51234/"

WS_TESTNET = "wss://" + TESTNET + ":51233/"
WS_DEVNET = "wss://" + DEVNET + ":51233/"
WS_MAINNET = "wss://" + MAINNET + "/"

REFERENCE_TX_COST = 10
ACCOUNT_DELETE_TX_COST = 2000000


class Client:
    """A json-rpc client class"""

    def __init__(self, url: str = RPC_MAINNET) -> None:
        """Return client instant, pass in network, defaults to mainnet"""
        self._url = url

    def json_rpc(self, payload: Any) -> Any:
        """calls the json_rpc api with requests returning json dict"""
        return json.loads(requests.post(self._url, json=payload).text)

    def fetch_status(self) -> Dict:
        # server_state
        payload = {"method": "server_state", "params": [{}]}
        result = self.json_rpc(payload).get("result")
        status = result.get("status")
        state = result.get("state")
        if state.get("server_state") == "disconnected":
            status = "shutdown"
        updated = int(
            datetime.datetime.strptime(state.get("time"), "%Y-%b-%d %H:%M:%S.%f %Z").timestamp()
            * 1000
        )
        return {"status": status, "updated": updated, "eta": "", "url": ""}

    def fetch_currencies(self, params: Dict) -> Dict:
        limit = int(params.get("limit", LIMIT))
        iteration = 0
        currencies: Any = {}
        marker = False
        has_next_page = True
        while iteration <= 5 and has_next_page:
            if marker is False:
                payload = {
                    "method": "ledger_data",
                    "params": [{"ledger_index": "validated", "binary": False, "limit": limit}],
                }
            else:
                payload = {
                    "method": "ledger_data",
                    "params": [
                        {
                            "ledger_index": "validated",
                            "binary": False,
                            "limit": limit,
                            "marker": marker,
                        }
                    ],
                }

            result = self.json_rpc(payload)
            state = result.get("result").get("state")
            state_count = len(state)
            if state_count < limit:
                has_next_page = False
            else:
                marker = result.get("result").get("marker")
            iteration += 1
            for item in state:
                if item.get("LedgerEntryType") == "RippleState":
                    balance = float(item.get("Balance").get("value", 0))
                    if balance == 0:
                        continue
                    elif balance > 0:
                        issuer = item.get("LowLimit").get("issuer")
                    elif balance < 0:
                        issuer = item.get("HighLimit").get("issuer")
                    currency = item.get("Balance").get("currency")
                    if currency not in currencies:
                        currencies[currency] = {"code": currency, "issuers": [issuer]}
                    else:
                        issuers_list: list = currencies[currency].get("issuers")
                        issuers_list.append(issuer)
        return currencies

    def fetch_balance(self, account: str) -> Dict:
        # gateway_balances
        payload = {"method": "gateway_balances", "params": [{"account": account}]}
        return self.json_rpc(payload)

    def fetch_fees(self) -> Dict:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return self.json_rpc(payload)

    def fetch_trading_fee(self) -> Dict:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return self.json_rpc(payload)

    def fetch_trading_fees(self) -> Dict:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return self.json_rpc(payload)

    def fetch_transaction_fee(self) -> Dict:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return self.json_rpc(payload)

    def fetch_transaction_fees(self) -> Dict:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return self.json_rpc(payload)

    def create_order(self) -> None:
        # offer_create
        print("create_order")

    def cancel_order(self) -> None:
        # offer_cancel
        print("cancel_order")

    def fetch_order_book(self, issuer: str) -> Dict:
        # book_offers
        payload = {
            "method": "book_offers",
            "params": [
                {
                    "taker_gets": {"currency": "XRP"},
                    "taker_pays": {"currency": "USD", "issuer": issuer},
                }
            ],
        }
        return self.json_rpc(payload)

    def fetch_trades(self, issuer: str) -> Dict:
        # book_offers
        payload = {
            "method": "book_offers",
            "params": [
                {
                    "taker_gets": {"currency": "XRP"},
                    "taker_pays": {"currency": "USD", "issuer": issuer},
                }
            ],
        }
        return self.json_rpc(payload)
