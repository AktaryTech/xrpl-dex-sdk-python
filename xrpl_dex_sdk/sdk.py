from dataclasses import dataclass
from typing import Any, Optional
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.asyncio.clients import AsyncJsonRpcClient, AsyncWebsocketClient
from xrpl.clients import JsonRpcClient

from . import methods
from .models import (
    Currencies,
    Issuers,
    Markets,
    TransferRates,
    BaseModel,
    REQUIRED,
    NetworkName,
)
from .constants import Networks, MAINNET


@dataclass(frozen=True)
class SDKParams(BaseModel):
    # xrpl servers
    network: NetworkName = REQUIRED
    json_rpc_url: Optional[str] = None
    ws_url: Optional[str] = None

    # clients
    client: Optional[AsyncJsonRpcClient] = None
    sync_client: Optional[JsonRpcClient] = None
    websocket_client: Optional[AsyncWebsocketClient] = None

    # wallet
    wallet: Optional[Wallet] = None
    wallet_secret: Optional[str] = None
    generate_wallet: Optional[bool] = False
    fund_testnet_wallet: Optional[bool] = False


class SDK:
    # clients
    client: AsyncJsonRpcClient
    sync_client: JsonRpcClient
    websocket_client: AsyncWebsocketClient

    # cache
    currencies: Optional[Currencies] = None
    issuers: Optional[Issuers] = None
    markets: Optional[Markets] = None
    transfer_rates: Optional[TransferRates] = None

    # state-changing methods
    cancel_order = methods.cancel_order
    create_limit_buy_order = methods.create_limit_buy_order
    create_limit_sell_order = methods.create_limit_sell_order
    create_order = methods.create_order
    create_trust_line = methods.create_trust_line

    # read-only methods
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
                network_urls["json_rpc"] if "json_rpc" in network_urls else params.json_rpc_url
            )
            if json_rpc_url == None:
                raise Exception("No JSON-RPC URL found or provided for network " + network + "!")
            self.client = AsyncJsonRpcClient(url=json_rpc_url)
        else:
            self.client = params.client

        if params.sync_client == None:
            json_rpc_url = (
                network_urls["json_rpc"] if "json_rpc" in network_urls else params.json_rpc_url
            )
            if json_rpc_url == None:
                raise Exception("No JSON-RPC URL found or provided for network " + network + "!")
            self.sync_client = JsonRpcClient(url=json_rpc_url)
        else:
            self.sync_client = params.sync_client

        if params.websocket_client == None:
            ws_url = network_urls["ws"] if "ws" in network_urls else params.ws_url
            if ws_url == None:
                raise Exception("No Websocket URL found or provided for network " + network + "!")
            self.websocket_client = AsyncWebsocketClient(url=ws_url)
        else:
            self.websocket_client = params.websocket_client

        if params.wallet == None:
            if params.wallet_secret == None:
                if params.generate_wallet == False:
                    raise Exception(
                        "Must provide a Wallet instance or a `wallet_secret`, or set `generate_wallet` to True"
                    )
                self.wallet = Wallet.create()
            else:
                wallet = Wallet(seed=params.wallet_secret, sequence=0)
                if wallet == None:
                    raise Exception("Could not create wallet using provided `wallet_secret`!")
                self.wallet = wallet
        else:
            self.wallet = params.wallet

        if params.fund_testnet_wallet == True:
            self.wallet = generate_faucet_wallet(client=self.sync_client, wallet=self.wallet)
