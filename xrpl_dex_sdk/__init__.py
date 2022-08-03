import json
from typing import Dict

import requests

# import websockets

__version__ = "0.1.0"
testnet = "https://s.altnet.rippletest.net:51234/"
mainnet = "https://xrplcluster.com"


class Client:
    """A json-rpc client class"""

    def json_rpc(self, payload: Dict) -> Dict:
        return json.loads(requests.post(self._url, json=payload).text)

    def __init__(self, url: str = mainnet) -> None:
        self._url = url

    def get_url(self) -> str:
        return self._url

    def fetch_balance(self, account: str) -> Dict:
        # gateway_balances
        payload = {"method": "gateway_balances", "params": [{"account": account}]}
        return self.json_rpc(payload)

    def fetch_status(self) -> Dict:
        # server_state
        payload = {"method": "server_state", "params": [{}]}
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
