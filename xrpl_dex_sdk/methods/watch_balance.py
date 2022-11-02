from typing import Any, Dict
import uuid

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import Subscribe, StreamParameter

from ..models import WatchBalanceParams
from ..utils import get_amount_currency_code


async def watch_balance(self, params: WatchBalanceParams) -> None:
    """
    Listens for new order book data for a single market pair.

    Parameters
    ----------
    params : xrpl_dex_sdk.models.WatchBalanceParams
        Additional request parameters
    """

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching balance: Websockets client not initialized")

    balance = await self.fetch_balance()

    account = self.wallet.classic_address
    payload = Subscribe(
        id=uuid.uuid4().hex,
        accounts=[account],
        streams=[StreamParameter.TRANSACTIONS, StreamParameter.LEDGER],
    )

    async def balance_handler(message: Any):
        if message["type"] == "ledgerClosed":
            if (
                balance != None
                and message["reserve_base"] != balance["info"]["validated_ledger"]["reserve_base"]
                or message["reserve_inc"] != balance["info"]["validated_ledger"]["reserve_inc"]
            ):
                return await self.fetch_balance()
        elif message["type"] == "transaction":
            transaction = message["transaction"]
            if transaction["TransactionType"] == "Payment":
                if transaction["Account"] == account or transaction["Destination"] == account:
                    return await self.fetch_balance()
            elif transaction["TransactionType"] == "OfferCreate":
                should_refresh = False
                if (
                    "code" in params
                    and get_amount_currency_code(transaction["TakerGets"]) != params.code
                    and get_amount_currency_code(transaction["TakerPays"]) != params.code
                ):
                    return
                elif transaction["Account"] == account:
                    should_refresh = True
                elif "meta" in transaction and "AffectedNodes" in transaction["meta"]:
                    # Were we affected by this txn?
                    for affected_node in transaction["meta"]["AffectedNodes"]:
                        node = (
                            affected_node["CreatedNode"]
                            if "CreatedNode" in affected_node
                            else affected_node["ModifiedNode"]
                            if "ModifiedNode" in affected_node
                            else affected_node["DeletedNode"]
                            if "DeletedNode" in affected_node
                            else None
                        )

                        if node == None:
                            continue

                        if node["LedgerEntryType"] == "AccountRoot" and (
                            "FinalFields" in node or "NewFields" in node
                        ):
                            if "code" in params and params.code != "XRP":
                                return
                            elif (
                                "FinalFields" in node and node["FinalFields"]["Account"] == account
                            ) or ("NewFields" in node and node["NewFields"]["Account"] == account):
                                should_refresh = True
                                break
                        elif node["LedgerEntryType"] == "RippleState" and (
                            "FinalFields" in node or "NewFields" in node
                        ):
                            if "code" in params:
                                if "FinalFields" in node:
                                    if (
                                        node["FinalFields"]["HighLimit"]["currency"] == params.code
                                        and node["FinalFields"]["LowLimit"]["currency"]
                                        == params.code
                                    ):
                                        should_refresh = True
                                        break
                                    if (
                                        node["FinalFields"]["HighLimit"]["issuer"] == account
                                        and node["FinalFields"]["LowLimit"]["issuer"] == account
                                    ):
                                        should_refresh = True
                                        break
                                elif "NewFields" in node:
                                    if (
                                        node["NewFields"]["HighLimit"]["currency"] == params.code
                                        and node["NewFields"]["LowLimit"]["currency"] == params.code
                                    ):
                                        should_refresh = True
                                        break
                                    if (
                                        node["NewFields"]["HighLimit"]["issuer"] == account
                                        and node["NewFields"]["LowLimit"]["issuer"] == account
                                    ):
                                        should_refresh = True
                                        break
                if should_refresh == True:
                    return await self.fetch_balance()

    async with self.websocket_client as websocket:
        await websocket.send(payload)
        initialized = False
        async for message in websocket:
            if initialized is False:
                if message.get("status") == "success":
                    initialized = True
                    continue
                else:
                    raise Exception(message)

            new_balance = await balance_handler(message)
            if new_balance != None:
                balance = new_balance
                if isinstance(params, Dict):
                    params["listener"](balance)
                else:
                    params.listener(balance)

    return {}
