from typing import Any, NamedTuple, Optional
from xrpl import clients, wallet

from . import methods
from .constants import Networks


class SDKParams(NamedTuple):
    network: str
    websockets_options: Optional[Any]
    wallet_secret: Optional[str]
    json_rpc_url: Optional[str]
    ws_url: Optional[str]


class SDK:
    # cancel_order = methods.cancel_order
    # create_limit_buy_order = methods.create_limit_buy_order
    # create_limit_sell_order = methods.create_limit_sell_order
    # create_order = methods.create_order
    # create_trust_line = methods.create_trust_line
    fetch_balance = methods.fetch_balance
    fetch_closed_orders = methods.fetch_closed_orders
    fetch_canceled_orders = methods.fetch_canceled_orders
    # fetch_currencies = methods.fetch_currencies
    # fetch_fees = methods.fetch_fees
    # fetch_issuers = methods.fetch_issuers
    # fetch_l2_order_book = methods.fetch_l2_order_book
    # fetch_market = methods.fetch_market
    # fetch_markets = methods.fetch_markets
    # fetch_my_trades = methods.fetch_my_trades
    fetch_open_orders = methods.fetch_open_orders
    fetch_order = methods.fetch_order
    # fetch_order_book = methods.fetch_order_book
    # fetch_order_books = methods.fetch_order_books
    fetch_orders = methods.fetch_orders
    # fetch_status = methods.fetch_status
    # fetch_ticker = methods.fetch_ticker
    # fetch_tickers = methods.fetch_tickers
    # fetch_trades = methods.fetch_trades
    # fetch_trading_fee = methods.fetch_trading_fee
    # fetch_trading_fees = methods.fetch_trading_fees
    # fetch_transaction_fee = methods.fetch_transaction_fee
    # fetch_transaction_fees = methods.fetch_transaction_fees
    # load_currencies = methods.load_currencies
    # load_issuers = methods.load_issuers
    # load_markets = methods.load_markets
    # watch_balance = methods.watch_balance
    # watch_my_trades = methods.watch_my_trades
    # watch_order_book = methods.watch_order_book
    # watch_orders = methods.watch_orders
    # watch_status = methods.watch_status
    # watch_ticker = methods.watch_ticker
    # watch_tickers = methods.watch_tickers
    # watch_trades = methods.watch_trades

    def __init__(self, params: SDKParams) -> None:

        if "wallet_secret" not in params:
            print("Must provide `wallet_secret`")
            return

        if "network" not in params and ("json_rpc_url" not in params and "ws_url" not in params):
            print("Must provide an XRPL network name or both `json_rpc_url` and `ws_url`")
            return

        json_rpc_url = (
            params["json_rpc_url"]
            if "json_rpc_url" in params
            else Networks[params["network"]]["json_rpc"]
            if params["network"] in Networks
            else None
        )
        if json_rpc_url == None:
            print("No JSON RPC URL defined!")
            return

        ws_url = (
            params["ws_url"]
            if "ws_url" in params
            else Networks[params["network"]]["ws"]
            if params["network"] in Networks
            else None
        )
        if ws_url == None:
            print("No Websockets URL defined!")
            return

        self.params = params
        self.client = clients.JsonRpcClient(json_rpc_url)
        self.wallet = wallet.Wallet(params["wallet_secret"], 0)
