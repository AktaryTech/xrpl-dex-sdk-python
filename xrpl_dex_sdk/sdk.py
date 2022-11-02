from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.asyncio.clients import AsyncJsonRpcClient, AsyncWebsocketClient
from xrpl.clients import JsonRpcClient

from xrpl_dex_sdk.methods import (
    cancel_order,
    create_limit_buy_order,
    create_limit_sell_order,
    create_order,
    create_trust_line,
    fetch_balance,
    fetch_closed_orders,
    fetch_canceled_orders,
    fetch_currencies,
    fetch_fees,
    fetch_issuers,
    fetch_l2_order_book,
    fetch_market,
    fetch_markets,
    fetch_my_trades,
    fetch_open_orders,
    fetch_order,
    fetch_order_book,
    fetch_order_books,
    fetch_orders,
    fetch_status,
    fetch_ticker,
    fetch_tickers,
    fetch_trades,
    fetch_trading_fee,
    fetch_trading_fees,
    fetch_transaction_fee,
    fetch_transaction_fees,
    fetch_transfer_rate,
    load_currencies,
    load_issuers,
    load_markets,
    watch_balance,
    watch_my_trades,
    watch_order_book,
    watch_orders,
    watch_status,
    watch_ticker,
    watch_tickers,
    watch_trades,
)
from xrpl_dex_sdk.models import (
    Currencies,
    Issuers,
    Markets,
    TransferRates,
    BaseModel,
    REQUIRED,
    NetworkName,
)
from xrpl_dex_sdk.constants import Networks, MAINNET, TESTNET, DEVNET


@dataclass(frozen=True)
class SDKParams(BaseModel):
    """
    Config parameters used when creating a new SDK instance.

    Attributes
    ----------
    network : NetworkName
        Name of the XRPL network to connect to.
    json_rpc_url : Optional[str]
        Custom JSON-RPC server URL. Will be ignored if network is not set to "custom".
    ws_url : Optional[str]
        Custom Websocket server URL. Will be ignored if network is not set to "custom".
    client : Optional[AsyncJsonRpcClient]
        Existing async JSON-RPC client instance. Must set network attribute to the network this client is connected to.
    sync_client : Optional[JsonRpcClient]
        Existing JSON-RPC client instance. Must set network attribute to the network this client is connected to.
    websocket_client : Optional[AsyncWebsocketClient]
        Existing Websocket client instance. Must set network attribute to the network this client is connected to.
    wallet : Optional[Wallet]
        Existing XRPL Wallet instance to use.
    wallet_secret : Optional[str]
        Secret value used to initialize an existing XRPL wallet.
    generate_wallet : Optional[bool]
        Whether to generate a new wallet. Will output the wallet's address, keys, and secret when done.
    fund_testnet_wallet : Optional[bool]
        Whether to fund a testnet account via a faucet. Will be ignored if network is not set to a testnet or devnet.
    """

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
    """
    The base XRPL dEX SDK class.

    Attributes
    ----------
    client : AsyncJsonRpcClient
        Client for making async calls to XRPL's JSON-RPC API.
    sync_client : JsonRpcClient
        Client for making synchronous calls to XRPL's JSON-RPC API.
    websocket_client : AsyncWebsocketClient
        Websocket client for subscribing to XRPL ledger updates.
    wallet : Wallet
        The SDK user's XRPL wallet.
    currencies : Optional[Currencies]
        Cached currency data.
    issuers : Optional[Issuers]
        Cached list of currency issuer data.
    markets : Optional[Markets]
        Cached list of markets data.
    transfer_rates : Optional[TransferRates]
        Cached transfer rates for currency issuers.
    """

    # clients
    client: AsyncJsonRpcClient
    sync_client: JsonRpcClient
    websocket_client: AsyncWebsocketClient

    # wallet
    wallet: Wallet

    # cache
    currencies: Optional[Currencies] = None
    issuers: Optional[Issuers] = None
    markets: Optional[Markets] = None
    transfer_rates: Optional[TransferRates] = None

    # state-changing methods
    cancel_order = cancel_order
    create_limit_buy_order = create_limit_buy_order
    create_limit_sell_order = create_limit_sell_order
    create_order = create_order
    create_trust_line = create_trust_line

    # read-only methods
    fetch_balance = fetch_balance
    fetch_closed_orders = fetch_closed_orders
    fetch_canceled_orders = fetch_canceled_orders
    fetch_currencies = fetch_currencies
    fetch_fees = fetch_fees
    fetch_issuers = fetch_issuers
    fetch_l2_order_book = fetch_l2_order_book
    fetch_market = fetch_market
    fetch_markets = fetch_markets
    fetch_my_trades = fetch_my_trades
    fetch_open_orders = fetch_open_orders
    fetch_order = fetch_order
    fetch_order_book = fetch_order_book
    fetch_order_books = fetch_order_books
    fetch_orders = fetch_orders
    fetch_status = fetch_status
    fetch_ticker = fetch_ticker
    fetch_tickers = fetch_tickers
    fetch_trades = fetch_trades
    fetch_trading_fee = fetch_trading_fee
    fetch_trading_fees = fetch_trading_fees
    fetch_transaction_fee = fetch_transaction_fee
    fetch_transaction_fees = fetch_transaction_fees
    fetch_transfer_rate = fetch_transfer_rate
    load_currencies = load_currencies
    load_issuers = load_issuers
    load_markets = load_markets
    watch_balance = watch_balance
    watch_my_trades = watch_my_trades
    watch_order_book = watch_order_book
    watch_orders = watch_orders
    watch_status = watch_status
    watch_ticker = watch_ticker
    watch_tickers = watch_tickers
    watch_trades = watch_trades

    def _is_testnet(self) -> bool:
        return (
            self.params
            and self.params.network
            and (self.params.network == TESTNET or self.params.network == DEVNET)
        )

    def __init__(self, params: Union[SDKParams, Dict[str, Any]]) -> None:
        params = params if isinstance(params, SDKParams) else SDKParams.from_dict(params)

        self.params = params

        # Specify a Network
        network = params.network if params.network != None else MAINNET
        network_urls = Networks[network]

        # Create async JSON-RPC client
        if params.client == None:
            json_rpc_url = (
                network_urls["json_rpc"] if "json_rpc" in network_urls else params.json_rpc_url
            )
            if json_rpc_url == None:
                raise Exception("No JSON-RPC URL found or provided for network " + network + "!")
            self.client = AsyncJsonRpcClient(url=json_rpc_url)
        else:
            self.client = params.client

        # Create synchronous JSON-RPC client
        if params.sync_client == None:
            json_rpc_url = (
                network_urls["json_rpc"] if "json_rpc" in network_urls else params.json_rpc_url
            )
            if json_rpc_url == None:
                raise Exception("No JSON-RPC URL found or provided for network " + network + "!")
            self.sync_client = JsonRpcClient(url=json_rpc_url)
        else:
            self.sync_client = params.sync_client

        # Create async Websocket client
        if params.websocket_client == None:
            ws_url = network_urls["ws"] if "ws" in network_urls else params.ws_url
            if ws_url == None:
                raise Exception("No Websocket URL found or provided for network " + network + "!")
            self.websocket_client = AsyncWebsocketClient(url=ws_url)
        else:
            self.websocket_client = params.websocket_client

        # self.wallet = self.generate_wallet()

        # Initialize wallet
        if not params.wallet and not params.wallet_secret and not params.generate_wallet:
            raise Exception(
                "Must provide a Wallet instance, a `wallet_secret`, or set `generate_wallet` to True"
            )

        if params.wallet:
            self.wallet = params.wallet
        elif params.wallet_secret:
            wallet = Wallet(seed=params.wallet_secret, sequence=0)
            if wallet == None:
                raise Exception("Could not create wallet using provided `wallet_secret`!")
            self.wallet = wallet
        elif params.generate_wallet:
            self.wallet = Wallet.create()

        # Fund wallet (testnet/devnet only)
        if params.fund_testnet_wallet and self._is_testnet():
            funded_wallet = generate_faucet_wallet(client=self.sync_client, wallet=self.wallet)
            if funded_wallet:
                self.wallet = funded_wallet


__all__ = ["SDKParams", "SDK"]
