from typing import Any, NamedTuple, Optional
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.asyncio.clients import AsyncJsonRpcClient, AsyncWebsocketClient
from xrpl.clients import JsonRpcClient

from . import methods
from .models import Currencies, Issuers, Markets, TransferRates
from .constants import Networks, NetworkName, MAINNET, LOCAL


class SDKParams(NamedTuple):
    network: Optional[str] = MAINNET
    # websockets_options: Optional[Any] = None
    wallet_secret: Optional[str] = None
    json_rpc_url: Optional[str] = None
    ws_url: Optional[str] = None
    client: Optional[JsonRpcClient] = None
    async_client: Optional[AsyncJsonRpcClient] = None
    websocket_client: Optional[AsyncWebsocketClient] = None
    wallet: Optional[Wallet] = None
    generate_wallet: Optional[bool] = False
    fund_testnet_wallet: Optional[bool] = False


class SDK:
    client: JsonRpcClient
    async_client: AsyncJsonRpcClient
    websocket_client: AsyncWebsocketClient
    # wallet: Optional[Wallet]
    # json_rpc_url: str
    # ws_url: str

    # cache
    currencies: Optional[Currencies] = None
    issuers: Optional[Issuers] = None
    markets: Optional[Markets] = None
    transfer_rates: Optional[TransferRates] = None

    cancel_order = methods.cancel_order
    create_limit_buy_order = methods.create_limit_buy_order
    create_limit_sell_order = methods.create_limit_sell_order
    create_order = methods.create_order
    create_trust_line = methods.create_trust_line
    fetch_balance = methods.fetch_balance
    fetch_closed_orders = methods.fetch_closed_orders
    fetch_canceled_orders = methods.fetch_canceled_orders
    fetch_currencies = methods.fetch_currencies
    fetch_fees = methods.fetch_fees
    fetch_issuers = methods.fetch_issuers
    fetch_l2_order_book = methods.fetch_l2_order_book
    fetch_market = methods.fetch_market
    fetch_markets = methods.fetch_markets
    fetch_my_trades = methods.fetch_my_trades
    fetch_open_orders = methods.fetch_open_orders
    fetch_order = methods.fetch_order
    fetch_order_book = methods.fetch_order_book
    fetch_order_books = methods.fetch_order_books
    fetch_orders = methods.fetch_orders
    fetch_status = methods.fetch_status
    fetch_ticker = methods.fetch_ticker
    fetch_tickers = methods.fetch_tickers
    fetch_trades = methods.fetch_trades
    fetch_trading_fee = methods.fetch_trading_fee
    fetch_trading_fees = methods.fetch_trading_fees
    fetch_transaction_fee = methods.fetch_transaction_fee
    fetch_transaction_fees = methods.fetch_transaction_fees
    fetch_transfer_rate = methods.fetch_transfer_rate
    load_currencies = methods.load_currencies
    load_issuers = methods.load_issuers
    load_markets = methods.load_markets
    watch_balance = methods.watch_balance
    watch_my_trades = methods.watch_my_trades
    watch_order_book = methods.watch_order_book
    watch_orders = methods.watch_orders
    watch_status = methods.watch_status
    watch_ticker = methods.watch_ticker
    watch_tickers = methods.watch_tickers
    watch_trades = methods.watch_trades

    def __init__(self, params: SDKParams) -> None:

        self.params = params

        # Specify a Network
        network = params.network if params.network != None else MAINNET
        network_urls = Networks[network]

        if params.client == None:
            json_rpc_url = (
                network_urls["json_rpc"]
                if "json_rpc" in network_urls
                else params.json_rpc_url
            )
            if json_rpc_url == None:
                raise Exception(
                    "No JSON-RPC URL found or provided for network " + network + "!"
                )
            self.client = JsonRpcClient(url=json_rpc_url)
        else:
            self.client = params.client

        if params.async_client == None:
            json_rpc_url = (
                network_urls["json_rpc"]
                if "json_rpc" in network_urls
                else params.json_rpc_url
            )
            if json_rpc_url == None:
                raise Exception(
                    "No JSON-RPC URL found or provided for network " + network + "!"
                )
            self.async_client = AsyncJsonRpcClient(url=json_rpc_url)
        else:
            self.async_client = params.async_client

        if params.websocket_client == None:
            ws_url = network_urls["ws"] if "ws" in network_urls else params.ws_url
            if ws_url == None:
                raise Exception(
                    "No Websocket URL found or provided for network " + network + "!"
                )
            self.websocket_client = AsyncWebsocketClient(url=ws_url)
        else:
            self.websocket_client = params.websocket_client

        if params.wallet == None:
            if params.wallet_secret == None:
                raise Exception(
                    "Must provide a Wallet instance or a `wallet_secret` parameter"
                )
            self.wallet = Wallet(seed=params.wallet_secret, sequence=0)
        else:
            self.wallet = params.wallet

        #   If Local, specify URLs
        #   If Custom, provide Clients
        # Provide a Wallet secret or a Wallet instance

        # if "wallet" not in params and "wallet_secret" not in params:
        #     print("Must either pass in a `Wallet` object or provide a `wallet_secret`")
        #     return

        # if (
        #     "network" not in params
        #     and "client" not in params
        #     and ("json_rpc_url" not in params and "ws_url" not in params)
        # ):
        #     print(
        #         "Must provide either an XRPL network name, both `json_rpc_url` and `ws_url`, or an XRPL `Client` object"
        #     )
        #     return

        # self.network = params.network if "network" in params else None

        # if params.json_rpc_url == None and (
        #     params.network == None
        #     or (params.network != None and getattr(Networks, params.network) == None)
        # ):
        #     raise Exception()

        # self.json_rpc_url = (
        #     params.json_rpc_url
        #     if params.json_rpc_url != None
        #     else (getattr(Networks, params.network)["json_rpc"])
        # )

        # if self.json_rpc_url != None and "network" not in params:
        #     for network in Networks:
        #         if Networks[network]["json_rpc"] == self.json_rpc_url:
        #             self.network = network
        #             break

        # self.ws_url = (
        #     params.ws_url
        #     if params.ws_url != None
        #     else (
        #         getattr(Networks, params.network)["ws"]
        #         if params.network in Networks
        #         else None
        #     )
        #     if "network" in params
        #     else None
        # )

        # if self.ws_url != None and "network" not in params:
        #     for network in Networks:
        #         if Networks[network]["ws"] == self.ws_url:
        #             self.network = network
        #             break

        # if params.client == None and self.json_rpc_url == None:
        #     raise Exception(
        #         "Could not create JSON-RPC client using provided credentials!"
        #     )

        # self.client = (
        #     params.client
        #     if params.client != None
        #     else AsyncJsonRpcClient(self.json_rpc_url)
        # )
        # self.json_rpc_client = self.client

        # self.websocket_client = (
        #     params.websocket_client
        #     if params.websocket_client != None
        #     else AsyncWebsocketClient(self.ws_url)
        #     if self.ws_url != None
        #     else None
        # )

        # if self.client == None:
        #     raise Exception(
        #         "Could not create JSON-RPC client using provided credentials!"
        #     )

        # self.wallet = (
        #     params.wallet
        #     if params.wallet != None
        #     else Wallet(params.wallet_secret, 0)
        #     if params.wallet_secret != None
        #     else None
        # )

        # if self.wallet == None:
        #     raise Exception("Could not create wallet using provided credentials!")

        # if params.fund_testnet_wallet != None and params.fund_testnet_wallet == True:
        #     self.wallet = generate_faucet_wallet(client=self.client, wallet=self.wallet)
