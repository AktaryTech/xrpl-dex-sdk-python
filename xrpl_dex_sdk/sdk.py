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
    fetch_balance = methods.fetch_balance
    fetch_order = methods.fetch_order
    fetch_orders = methods.fetch_orders
    fetch_open_orders = methods.fetch_open_orders
    fetch_closed_orders = methods.fetch_closed_orders
    fetch_canceled_orders = methods.fetch_canceled_orders

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
