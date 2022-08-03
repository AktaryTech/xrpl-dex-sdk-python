import requests

# import websockets

__version__ = "0.1.0"
testnet = "https://s.altnet.rippletest.net:51234/"
mainnet = "https://xrplcluster.com"


class Client:
    """A json-rpc client class"""

    def __init__(self, url: str = mainnet) -> None:
        self._url = url

    def get_url(self) -> str:
        return self._url

    def fetch_balance(self, account: str) -> requests.Response:
        # gateway_balances
        payload = {"method": "gateway_balances", "params": [{"account": account}]}
        return requests.post(self._url, json=payload)

    def fetch_status(self) -> requests.Response:
        # server_state
        payload = {"method": "server_state", "params": [{}]}
        return requests.post(self._url, json=payload)

    def fetch_fees(self) -> requests.Response:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return requests.post(self._url, json=payload)

    def fetch_trading_fee(self) -> requests.Response:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return requests.post(self._url, json=payload)

    def fetch_trading_fees(self) -> requests.Response:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return requests.post(self._url, json=payload)

    def fetch_transaction_fee(self) -> requests.Response:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return requests.post(self._url, json=payload)

    def fetch_transaction_fees(self) -> requests.Response:
        # fee
        payload = {"method": "fee", "params": [{}]}
        return requests.post(self._url, json=payload)

    def create_order(self) -> None:
        # offer_create
        print("create_order")

    def cancel_order(self) -> None:
        # offer_cancel
        print("cancel_order")

    def fetch_order_book(self, issuer: str) -> requests.Response:
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
        return requests.post(self._url, json=payload)

    def fetch_trades(self, issuer: str) -> requests.Response:
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
        return requests.post(self._url, json=payload)
