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

    def load_data(self, name: str) -> Dict:
        path = os.path.dirname(os.path.realpath(__file__)) + os.sep + "data" + os.sep + name
        f = open(path, "r")
        data = f.read()
        f.close()
        return json.loads(data)

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

    def fetch_currencies(self) -> Dict:
        return self.load_data("currencies.json")

    def fetch_markets(self) -> Dict:
        return self.load_data("markets.json")

    def fetch_issuers(self) -> Dict:
        return self.load_data("issuers.json")

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

    def fetch_order_books(self, symbols: list[str], limit: float = LIMIT, params: Any = {}) -> Dict:
        order_books: Any = {}
        for symbol in symbols:
            order_books.setdefault(symbol, self.fetch_order_book(symbol, limit, params.get(symbol)))
        return order_books

    def fetch_order_book(self, symbol: str, limit: float = LIMIT, params: Any = {}) -> Dict:
        [base, quote] = symbol.split("/")
        taker_pays = {
            "currency": quote,
        }
        if "taker_pays_issuer" in params:
            taker_pays["issuer"] = params.get("taker_pays_issuer")

        taker_gets = {
            "currency": base,
        }
        if "taker_gets_issuer" in params:
            taker_gets["issuer"] = params.get("taker_gets_issuer")

        # book_offers
        payload: Any = {
            "method": "book_offers",
            "params": [
                {
                    "taker_gets": taker_gets,
                    "taker_pays": taker_pays,
                    "limit": limit,
                }
            ],
        }

        if "ledger_index" in params:
            payload.get("params")[0]["ledger_index"] = params.get("ledger_index")

        if "ledger_hash" in params:
            payload.get("params")[0]["ledger_hash"] = params.get("ledger_hash")

        if "taker" in params:
            payload.get("params")[0]["taker"] = params.get("taker")

        result = self.json_rpc(payload)

        offers = result.get("result").get("offers")
        bids: Any = []
        asks: Any = []
        nonce = offers[-1].get("Sequence")

        for offer in offers:
            if offer.get("Flags") & 131072 == 0:
                if "value" in offer.get("TakerGets"):
                    bids.append([offer.get("quality"), offer.get("TakerGets").get("value")])
                else:
                    bids.append([offer.get("quality"), float(offer.get("TakerGets"))])
            else:
                if "value" in offer.get("TakerGets"):
                    asks.append([offer.get("quality"), offer.get("TakerGets").get("value")])
                else:
                    asks.append([offer.get("quality"), float(offer.get("TakerGets"))])

        return {
            "symbol": symbol,
            "nonce": nonce,
            "bids": bids,
            "asks": asks,
        }

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
