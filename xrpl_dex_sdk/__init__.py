import datetime
import json
from typing import Any, Dict

import requests

# import websockets

__version__ = "0.1.0"
testnet = "https://s.altnet.rippletest.net:51234/"
mainnet = "https://xrplcluster.com"


class Client:
    """A json-rpc client class"""

    def __init__(self, url: str = mainnet) -> None:
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

    # def create_order(
    #     self, symbol: str, side: str, type: str, amount: str, price: str, params
    # ) -> Dict:
    #     # gateway_balances
    #     payload = {"method": "gateway_balances", "params": [{"account": account}]}
    #     return self.json_rpc(payload)

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
