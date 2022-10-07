from typing import Any, NamedTuple, Optional
from xrpl import clients, wallet

from . import methods
from .constants import Networks


class SDKParams(NamedTuple):
    network: Optional[str]
    websockets_options: Optional[Any]
    wallet_secret: Optional[str]
    json_rpc_url: Optional[str]
    ws_url: Optional[str]
    client: Optional[clients.JsonRpcClient]
    wallet: Optional[wallet.Wallet]
    fund_testnet_wallet: Optional[bool] = False


class SDK:
    cancel_order = methods.cancel_order
    create_limit_buy_order = methods.create_limit_buy_order
    create_limit_sell_order = methods.create_limit_sell_order
    create_order = methods.create_order
    # create_trust_line = methods.create_trust_line
    fetch_balance = methods.fetch_balance
    fetch_closed_orders = methods.fetch_closed_orders
    fetch_canceled_orders = methods.fetch_canceled_orders
    fetch_currencies = methods.fetch_currencies
    # fetch_fees = methods.fetch_fees
    fetch_issuers = methods.fetch_issuers
    # fetch_l2_order_book = methods.fetch_l2_order_book
    # fetch_market = methods.fetch_market
    fetch_markets = methods.fetch_markets
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
    fetch_trading_fee = methods.fetch_trading_fee
    fetch_trading_fees = methods.fetch_trading_fees
    fetch_transaction_fee = methods.fetch_transaction_fee
    fetch_transaction_fees = methods.fetch_transaction_fees
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

        if "wallet" not in params and "wallet_secret" not in params:
            print("Must either pass in a `Wallet` object or provide a `wallet_secret`")
            return

        if (
            "network" not in params
            and "client" not in params
            and ("json_rpc_url" not in params and "ws_url" not in params)
        ):
            print(
                "Must provide either an XRPL network name, both `json_rpc_url` and `ws_url`, or an XRPL `Client` object"
            )
            return

        self.json_rpc_url = (
            params["json_rpc_url"]
            if "json_rpc_url" in params
            else (
                Networks[params["network"]]["json_rpc"]
                if params["network"] in Networks
                else None
            )
            if "network" in params
            else None
        )

        self.ws_url = (
            params["ws_url"]
            if "ws_url" in params
            else (
                Networks[params["network"]]["ws"]
                if params["network"] in Networks
                else None
            )
            if "network" in params
            else None
        )

        self.params = params

        self.client = (
            params["client"]
            if "client" in params
            else clients.JsonRpcClient(self.json_rpc_url)
        )

        self.wallet = (
            params["wallet"]
            if "wallet" in params
            else wallet.Wallet(params["wallet_secret"], 0)
        )

        if (
            self.wallet != None
            and "fund_testnet_wallet" in params
            and params["fund_testnet_wallet"] == True
        ):
            self.wallet = wallet.generate_faucet_wallet(
                client=self.client, wallet=self.wallet
            )
