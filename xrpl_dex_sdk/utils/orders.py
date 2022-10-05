import json
from re import I
from typing import Any, List

from xrpl.clients import JsonRpcClient
from xrpl.models.requests.ledger_entry import Offer
from xrpl.models.requests.tx import Tx
from xrpl.models.requests.account_tx import AccountTx

from ..constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT
from ..models.ccxt.orders import OrderId, OrderSide, OrderStatus
from ..models.ccxt.trades import TradeTakerOrMaker, TradeSide
from ..models.xrpl.offers import OfferFlags
from ..models.xrpl.transactions import Node, TransactionMetadata
from ..utils.hashes import hash_offer_id


def get_taker_or_maker(side: TradeSide) -> TradeTakerOrMaker:
    return TradeTakerOrMaker.Maker if side == TradeSide.Sell else TradeTakerOrMaker.Taker


def get_order_side_from_offer(offer: Offer) -> OrderSide:
    return "sell" if (offer.Flags & OfferFlags.LSF_SELL) == OfferFlags.LSF_SELL else "buy"


def get_base_amount_key(side: OrderSide or TradeSide) -> str:
    return "TakerPays" if (side == OrderSide.Buy or side == TradeSide.Buy) else "TakerGets"


def get_quote_amount_key(side: OrderSide or TradeSide) -> str:
    return "TakerGets" if (side == OrderSide.Buy or side == TradeSide.Buy) else "TakerPays"


#
# Returns an Offer Ledger object from an AffectedNode
#
def get_offer_from_node(node: Node) -> Offer:
    PreviousTxnID, LedgerIndex, LedgerEntryType, FinalFields, PreviousFields = node[0]

    if LedgerEntryType != "Offer" or FinalFields == None:
        return

    offer = FinalFields

    offer["index"] = LedgerIndex
    offer["PreviousTxnID"] = (
        FinalFields["PreviousTxnID"] if FinalFields["PreviousTxnID"] != None else PreviousTxnID
    )
    offer["TakerGets"] = (
        PreviousFields["TakerGets"]["amount"] - FinalFields["TakerGets"]["amount"]
        if PreviousFields != None
        else FinalFields["TakerGets"]
    )
    offer["TakerPays"] = (
        PreviousFields["TakerPays"]["amount"] - FinalFields["TakerPays"]["amount"]
        if PreviousFields != None
        else FinalFields["TakerPays"]
    )

    return offer


#
# Returns an Offer Ledger object from a Transaction
#
def get_offer_from_tx(transaction: Any) -> Offer:
    if transaction["TransactionType"] != "OfferCreate":
        return

    Account, Flags, Sequence, TakerGets, TakerPays = transaction

    if Sequence == None:
        return

    offer = {
        "Account": Account,
        "BookDirectory": "",
        "BookNode": "0",
        "LedgerEntryType": "Offer",
        "Flags": Flags,
        "OwnerNode": "0",
        "Sequence": Sequence,
        "TakerGets": TakerGets,
        "TakerPays": TakerPays,
        "index": hash_offer_id(Account, Sequence),
        "PreviousTxnID": "",
        "PreviousTxnLgrSeq": 0,
    }

    return offer


#
# Parse a Transaction and return the important data
#
def parse_transaction(id: OrderId, transaction: Any) -> Any:
    offer_ledger_index = hash_offer_id(id.account, id.sequence)
    print("offer_ledger_index")
    print(offer_ledger_index)

    previous_txn_hash: str or None
    tx: Any
    metadata: str or TransactionMetadata or None

    if "result" in transaction:
        if transaction["result"]["TransactionType"] != "OfferCreate":
            return
        tx = transaction["result"]
        metadata = tx["meta"]

    elif "tx" in transaction:
        if transaction["tx"]["TransactionType"] != "OfferCreate":
            return
        tx = transaction["tx"]
        metadata = transaction["meta"]
    elif "metaData" in transaction:
        if transaction["TransactionType"] != "OfferCreate":
            return
        metaData, *ledgerTx = transaction
        tx = ledgerTx
        metadata = metaData

    print("tx")
    print(tx)
    print("metadata")
    print(metadata)

    if "hash" not in tx or tx["TransactionType"] != "OfferCreate" or metadata == str:
        return

    trade_offers: List[Offer] = []
    parsed_nodes: List[Node] = []

    if tx["Account"] == id.account and tx["Sequence"] == id.sequence:
        for affected_node in metadata["AffectedNodes"]:
            offer = get_offer_from_node(affected_node)
            if offer != None and offer["Account"] != id.account:
                trade_offers.append(offer)
                parsed_nodes.append(affected_node)

        previous_txn_hash = None
    elif tx["Account"] != id.account:
        for affected_node in metadata["AffectedNodes"]:
            offer = get_offer_from_node(affected_node)
            if offer != None and offer["index"] == offer_ledger_index:
                previous_txn_hash = offer["PreviousTxnID"]

                trade_offer = get_offer_from_tx(tx)
                if trade_offer == None:
                    return

                trade_offer["PreviousTxnID"] = offer["PreviousTxnID"]
                trade_offer["TakerGets"] = offer["TakerGets"]
                trade_offer["TakerPays"] = offer["TakerPays"]

                trade_offers.append(trade_offer)
                parsed_nodes.append(affected_node)

    meta, *txData = tx

    metadata["AffectedNodes"] == parsed_nodes

    return {
        "transaction": txData,
        "metadata": metadata,
        "offers": trade_offers,
        "previous_txn_id": previous_txn_hash,
        "date": tx["date"] if tx["date"] != None else 0,
    }


#
# Get the ID of the most recent Transaction to affect an Order
#
async def get_most_recent_tx_id(
    client: JsonRpcClient,
    id: OrderId,
    # This is to prevent us spending forever searching through an account's Transactions for an Order
    search_limit: int = DEFAULT_SEARCH_LIMIT,
) -> str or None:
    ledger_offer_request = Offer.from_dict(
        {"account": id.account, "sequence": id.sequence, "ledger_index": "validated"}
    )
    ledger_offer_response = await client.request(ledger_offer_request)
    ledger_offer_result = ledger_offer_response.result

    if ledger_offer_result != None:
        ledger_offer = json.dumps(ledger_offer_result.node, indent=4, sort_keys=True)
        return ledger_offer["PreviousTxnID"]
    else:
        limit = DEFAULT_LIMIT
        marker: Any
        has_next_page = True
        page = 1

        while has_next_page == True:
            account_tx_request = AccountTx.from_dict(
                {"account": id.account, "ledger_index": "validated"}
            )
            account_tx_response = await client.request(account_tx_request)
            account_tx_result = account_tx_response.result

            if account_tx_result == None:
                return

            account_tx = json.dumps(account_tx_result.transactions, indent=4, sort_keys=True)
            print(account_tx)

            marker = account_tx_result.marker

            for tx in account_tx:
                previous_txn_data = parse_transaction(id, tx)
                if previous_txn_data != None:
                    return previous_txn_data["previous_txn_id"]

            if marker == None or limit * page >= search_limit:
                has_next_page = False
            else:
                page += 1


#
# Get the most recent Transaction to affect an Order
#
async def get_most_recent_tx(
    client: JsonRpcClient,
    id: OrderId,
    # This is to prevent us spending forever searching through an account's Transactions for an Order
    search_limit: int = DEFAULT_SEARCH_LIMIT,
) -> Any or None:
    order_status = OrderStatus.Open

    ledger_offer_request = Offer.from_dict(
        {"account": id.account, "sequence": id.sequence, "ledger_index": "validated"}
    )
    ledger_offer_response = await client.request(ledger_offer_request)
    ledger_offer_result = ledger_offer_response.result

    if ledger_offer_result != None:
        ledger_offer = json.dumps(ledger_offer_result.node, indent=4, sort_keys=True)

        print("ledger_offer")
        print(ledger_offer)

        tx_request = Tx.from_dict(
            {"transaction": ledger_offer["PreviousTxnID"], "ledger_index": "validated"}
        )
        tx_response = await client.request(tx_request)
        tx_result = tx_response.result

        if tx_result != None:
            tx = json.dumps(tx_result.node, indent=4, sort_keys=True)
            previous_txn_data = parse_transaction(id, tx)
            if previous_txn_data != None:
                return {
                    "previous_txn_data": previous_txn_data,
                    "previous_txn_id": previous_txn_data["previous_txn_id"],
                    "order_status": order_status,
                }
    else:
        order_status = OrderStatus.Closed

        limit = DEFAULT_LIMIT
        marker: Any
        has_next_page = True
        page = 1

        while has_next_page == True:
            account_tx_request = AccountTx.from_dict(
                {"account": id.account, "ledger_index": "validated"}
            )
            account_tx_response = await client.request(account_tx_request)
            account_tx_result = account_tx_response.result

            if account_tx_result == None:
                return

            account_tx = json.dumps(account_tx_result.transactions, indent=4, sort_keys=True)
            print(account_tx)

            marker = account_tx_result.marker

            for tx in account_tx:
                previous_txn_data = parse_transaction(id, tx)
                if previous_txn_data != None:
                    return {
                        "previous_txn_data": previous_txn_data,
                        "previous_txn_id": previous_txn_data["previous_txn_id"],
                        "order_status": order_status,
                    }

            if marker == None or limit * page >= search_limit:
                has_next_page = False
            else:
                page += 1
