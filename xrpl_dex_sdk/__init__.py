import datetime
import json
import os
from typing import Any, Dict

import requests

# import websockets

__version__ = "0.1.0"

# const
LIMIT: int = int(os.getenv("RIPPLE_DEFAULT_LIMIT", 20))

TESTNET: str = os.getenv("RIPPLE_TESTNET_URL", "s.altnet.rippletest.net")
DEVNET: str = os.getenv("RIPPLE_DEVNET_URL", "s.devnet.rippletest.net")
MAINNET: str = os.getenv("RIPPLE_MAINNET_URL", "s1.ripple.com")

RPC_TESTNET: str = "https://" + TESTNET + ":51234/"
RPC_DEVNET: str = "https://" + DEVNET + ":51234/"
RPC_MAINNET: str = "https://" + MAINNET + ":51234/"

WS_TESTNET: str = "wss://" + TESTNET + ":51233/"
WS_DEVNET: str = "wss://" + DEVNET + ":51233/"
WS_MAINNET: str = "wss://" + MAINNET + "/"

REFERENCE_TX_COST: int = 10
ACCOUNT_DELETE_TX_COST: int = 2000000

BILLION: int = 1000000000


class Client:
    """A json-rpc client class"""

    def __init__(self, url: str = RPC_MAINNET) -> None:
        """Return client instant, pass in network, defaults to mainnet"""
        self._cache: Any = {}
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

    def transfer_rate_to_decimal(self, rate: int) -> str:
        if rate != int(rate):
            raise Exception("Error decoding, transfer Rate must be an integer")

        if rate == 0:
            return "0"

        decimal = (rate - BILLION) / BILLION

        if decimal < 0:
            raise Exception("Error decoding, negative transfer rate")

        return str(decimal)

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
        if "fetch_currencies" in self._cache:
            return self._cache.get("fetch_currencies")
        currencies = self.load_data("currencies.json")
        for _, currency in currencies.items():
            for curr in currency:
                payload = {"method": "account_info", "params": [{"account": curr.get("issuer")}]}
                account_info_result = self.json_rpc(payload).get("result")
                account_rate = account_info_result.get("account_data").get("TransferRate")
                if account_rate:
                    curr["fee"] = self.transfer_rate_to_decimal(account_rate)
        self._cache["fetch_currencies"] = currencies
        return currencies

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

    def fetch_trading_fee(self, symbol: str) -> Dict:
        markets = self.fetch_markets()
        if symbol in markets is False:
            raise Exception("No symbol in markets data")

        market_symbol: Any = markets.get(symbol)
        base_fee = market_symbol.get("baseFee", 0)
        base_issuer = market_symbol.get("baseIssuer")
        quote_fee = market_symbol.get("quoteFee", 0)
        quote_issuer = market_symbol.get("quoteIssuer")
        response: Any = {
            "symbol": symbol,
            "base": base_fee,
            "quote": quote_fee,
            "percentage": True,
            "info": json.dumps({"market": market_symbol}),
        }
        if base_issuer:
            response["baseIssuer"] = base_issuer
        if quote_issuer:
            response["quoteIssuer"] = quote_issuer

        return response

    def fetch_trading_fees(self) -> list:
        markets = self.fetch_markets()
        result: list = []
        for market in markets:
            result.append(self.fetch_trading_fee(market))
        return result

    def fetch_transaction_fee(self, code: str, params: Dict = {}) -> Dict:
        payload = {"method": "fee", "params": [{}]}
        fees_result = self.json_rpc(payload).get("result")

        currencies = self.fetch_currencies()
        if code in currencies is False:
            raise Exception("No code in currencies data")

        transfer_rates: Any = {}

        currency: Any = currencies.get(code)

        params_issuer = params.get("issuer")
        for curr in currency:
            fee = curr.get("fee", 0)
            issuer = curr.get("issuer")
            if "issuer" in params:
                if params_issuer == issuer:
                    transfer_rates[issuer] = fee
            else:
                transfer_rates[issuer] = fee

        response: Any = {
            "code": code,
            "current": int(fees_result.get("drops").get("open_ledger_fee")),
            "transfer": transfer_rates,
            "info": json.dumps({"feesResult": fees_result, "currency": currency}),
        }

        return response

    def fetch_transaction_fees(self, codes: list, params: dict = {}) -> list:
        response: list = []
        for code in codes:
            param = params.get("code", {})
            response.append(self.fetch_transaction_fee(code, param))
        return response

    def create_order(self) -> None:
        # offer_create
        print("create_order")

    def cancel_order(self) -> None:
        # offer_cancel
        print("cancel_order")

    def fetch_order_books(self, symbols: list, limit: float = LIMIT, params: Any = {}) -> Dict:
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
