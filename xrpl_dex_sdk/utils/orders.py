import json
from typing import Any, Dict, List, NamedTuple, Optional, Union

from xrpl.clients import JsonRpcClient
from xrpl.models.requests.ledger_entry import LedgerEntry
from xrpl.models.requests.tx import Tx
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.requests.account_tx import AccountTx
from xrpl.utils import posix_to_ripple_time, drops_to_xrp


from ..constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT
from ..models import (
    LedgerEntryTypes,
    CurrencyCode,
    OrderId,
    OrderSide,
    OrderStatus,
    TradeTakerOrMaker,
    TradeSide,
    Offer,
    OfferCreateFlags,
    OfferFlags,
    Node,
    TransactionMetadata,
)
from ..utils import hash_offer_id, omit, sort_by_date, subtract_amounts


def order_to_json(input: NamedTuple) -> str:
    output: Dict[str, Any] = {}
    for field in input._fields:
        if field == "fee":
            if input.__getattribute__(field) == None:
                continue
            else:
                output[field] = input.__getattribute__(field)
        if field == "trades":
            trades = []
            for _trade in input.__getattribute__(field):
                trade: Dict[str, Any] = {}
                for trade_field in _trade._fields:
                    if trade_field == "info" or trade_field == "fee":
                        trade[trade_field] = _trade.__getattribute__(trade_field)
                    else:
                        trade[trade_field] = str(_trade.__getattribute__(trade_field))
                trades.append(trade)
            output[field] = trades
        elif field == "info" or field == "timestamp" or field == "lastTradeTimestamp":
            output[field] = input.__getattribute__(field)
        else:
            output[field] = str(input.__getattribute__(field))
    return json.dumps(output)


def set_transaction_flags_to_number(tx: Any):
    if "Flags" not in tx or tx["Flags"] == None:
        tx["Flags"] = 0
        return tx

    elif isinstance(tx["Flags"], int):
        return tx

    else:
        if tx["TransactionType"] == "OfferCreate":
            flags = 0
            for flag in tx["Flags"]:
                print("flag")
                print(flag)
                if OfferCreateFlags.__getattribute__(flag) != None:
                    flags = tx["Flags"] | OfferCreateFlags.__getattribute__(flag)
            tx["Flags"] = flags
            return tx


def get_taker_or_maker(side: TradeSide) -> TradeTakerOrMaker:
    return (
        TradeTakerOrMaker.Maker if side == TradeSide.Sell else TradeTakerOrMaker.Taker
    )


def get_order_side(flags: int) -> OrderSide:
    if flags & OfferFlags.LSF_SELL.value == OfferFlags.LSF_SELL.value:
        return OrderSide.Sell
    elif flags & OfferCreateFlags.TF_SELL.value == OfferCreateFlags.TF_SELL.value:
        return OrderSide.Sell
    else:
        return OrderSide.Buy


def get_order_side_from_offer(offer: Offer) -> OrderSide:
    return (
        "sell" if (offer.Flags & OfferFlags.LSF_SELL) == OfferFlags.LSF_SELL else "buy"
    )


def get_amount_currency_code(amount: Union[IssuedCurrencyAmount, str]):
    return (
        CurrencyCode(amount["currency"], amount["issuer"])
        if "currency" in amount
        else CurrencyCode("XRP")
    )


def get_base_amount_key(side: OrderSide or TradeSide) -> str:
    return (
        "TakerPays" if (side == OrderSide.Buy or side == TradeSide.Buy) else "TakerGets"
    )


def get_quote_amount_key(side: OrderSide or TradeSide) -> str:
    return (
        "TakerGets" if (side == OrderSide.Buy or side == TradeSide.Buy) else "TakerPays"
    )


def get_offer_base_value(offer: Offer) -> float:
    amount = (
        offer["TakerPays"]
        if offer["Flags"] & OfferFlags.LSF_SELL.value == 0
        else offer["TakerGets"]
    )
    return float(amount["value"] if "value" in amount else drops_to_xrp(amount))


def get_offer_quote_value(offer: Offer) -> float:
    quote_amount = (
        offer["TakerGets"]
        if offer["Flags"] & OfferFlags.LSF_SELL.value == 0
        else offer["TakerPays"]
    )
    return float(
        quote_amount["value"] if "value" in quote_amount else drops_to_xrp(quote_amount)
    )


def get_book_offer_taker_pays(book_offer: Offer):
    return (
        book_offer["taker_pays_funded"]
        if "taker_pays_funded" in book_offer
        else book_offer["TakerPays"]
    )


def get_book_offer_taker_gets(book_offer: Offer):
    return (
        book_offer["taker_gets_funded"]
        if "taker_gets_funded" in book_offer
        else book_offer["TakerGets"]
    )


def get_book_offer_base_value(book_offer: Offer) -> float:
    amount = (
        get_book_offer_taker_pays(book_offer)
        if book_offer["Flags"] & OfferFlags.LSF_SELL.value == 0
        else get_book_offer_taker_gets(book_offer)
    )
    return float(amount["value"] if "value" in amount else drops_to_xrp(amount))


def get_book_offer_quote_value(book_offer: Offer) -> float:
    quote_amount = (
        get_book_offer_taker_gets(book_offer)
        if book_offer["Flags"] & OfferFlags.LSF_SELL.value == 0
        else get_book_offer_taker_pays(book_offer)
    )
    return float(
        quote_amount["value"] if "value" in quote_amount else drops_to_xrp(quote_amount)
    )


#
# Returns an Offer Ledger object from an AffectedNode
#
def get_offer_from_node(node: Node) -> Offer:
    node_type = list(node.keys())[0]

    affected_node = node[node_type]

    if (
        affected_node["LedgerEntryType"] != LedgerEntryTypes.Offer.value
        or "FinalFields" not in affected_node
    ):
        return

    LedgerIndex = affected_node["LedgerIndex"]
    FinalFields = affected_node["FinalFields"]
    PreviousTxnID = (
        affected_node["PreviousTxnID"] if "PreviousTxnID" in affected_node else None
    )
    PreviousFields = (
        affected_node["PreviousFields"] if "PreviousFields" in affected_node else None
    )

    offer_index = LedgerIndex
    offer_previous_txn_id = (
        FinalFields["PreviousTxnID"]
        if "PreviousTxnID" in FinalFields
        else PreviousTxnID
    )

    offer_taker_gets = (
        subtract_amounts(PreviousFields["TakerGets"], FinalFields["TakerGets"])
        if PreviousFields != None
        else FinalFields["TakerGets"]
    )
    offer_taker_pays = (
        subtract_amounts(PreviousFields["TakerPays"], FinalFields["TakerPays"])
        if PreviousFields != None
        else FinalFields["TakerPays"]
    )

    offer = Offer(
        Account=FinalFields["Account"],
        BookDirectory="",
        BookNode="0",
        Flags=FinalFields["Flags"],
        LedgerEntryType=LedgerEntryTypes.Offer.value,
        OwnerNode="0",
        PreviousTxnID=offer_previous_txn_id,
        PreviousTxnLgrSeq=0,
        Sequence=FinalFields["Sequence"],
        TakerGets=offer_taker_gets,
        TakerPays=offer_taker_pays,
        index=offer_index,
        Expiration=None,
    )

    return offer


#
# Returns an Offer Ledger object from a Transaction
#
def get_offer_from_tx(
    transaction: Any, overrides: Optional[Dict[str, Any]] = {}
) -> Offer:
    if transaction["TransactionType"] != "OfferCreate":
        return

    Account = overrides["Account"] if "Account" in overrides else transaction["Account"]
    Flags = overrides["Flags"] if "Flags" in overrides else transaction["Flags"]
    Sequence = (
        overrides["Sequence"]
        if "Sequence" in overrides
        else transaction["Sequence"]
        if "Sequence" in transaction
        else None
    )
    TakerGets = (
        overrides["TakerGets"] if "TakerGets" in overrides else transaction["TakerGets"]
    )
    TakerPays = (
        overrides["TakerPays"] if "TakerPays" in overrides else transaction["TakerPays"]
    )
    PreviousTxnID = overrides["PreviousTxnID"] if "PreviousTxnID" in overrides else ""

    if Sequence == None:
        return

    offer = Offer(
        Account=Account,
        BookDirectory="",
        BookNode="0",
        Flags=Flags,
        LedgerEntryType=LedgerEntryTypes.Offer.value,
        OwnerNode="0",
        PreviousTxnID=PreviousTxnID,
        PreviousTxnLgrSeq=0,
        Sequence=Sequence,
        TakerGets=TakerGets,
        TakerPays=TakerPays,
        index=hash_offer_id(Account, Sequence),
        Expiration=None,
    )

    return offer


#
# Parse a Transaction and return the important data
#
def parse_transaction(id: OrderId, transaction: Any) -> Dict[str, Any]:
    offer_ledger_index = hash_offer_id(id.account, id.sequence)

    previous_txn_hash: str or None = None
    tx: Any or None = None
    metadata: str or TransactionMetadata or None

    if "result" in transaction:
        if transaction["result"]["TransactionType"] != "OfferCreate":
            return
        tx = transaction["result"]
        metadata = transaction["meta"]
    elif "tx" in transaction:
        if transaction["tx"]["TransactionType"] != "OfferCreate":
            return
        tx = transaction["tx"]
        metadata = transaction["meta"]
    elif "metaData" in transaction:
        if transaction["TransactionType"] != "OfferCreate":
            return
        tx = omit(transaction, {"metaData"})
        metadata = transaction["metaData"]
    elif "meta" in transaction:
        if transaction["TransactionType"] != "OfferCreate":
            return
        tx = omit(transaction, {"meta"})
        metadata = transaction["meta"]

    if tx == None:
        print("Could not get Transaction data! Skipping...")
        return
    if "hash" not in tx:
        print('Property "hash" not found on Transaction! Skipping...')
        return
    if isinstance(metadata, str):
        print("Metadata is not an object! Skipping...")
        return

    trade_offers: List[Offer] = []

    if tx["Account"] == id.account and tx["Sequence"] == id.sequence:
        for affected_node in metadata["AffectedNodes"]:
            offer = get_offer_from_node(affected_node)
            if offer != None and offer.Account != id.account:
                trade_offers.append(offer)
        previous_txn_hash = None
    elif tx["Account"] != id.account:
        for affected_node in metadata["AffectedNodes"]:
            offer = get_offer_from_node(affected_node)
            if offer != None and offer.index == offer_ledger_index:
                previous_txn_hash = offer.PreviousTxnID

                trade_offer = get_offer_from_tx(
                    tx,
                    {
                        "PreviousTxnID": offer.PreviousTxnID,
                        "TakerGets": offer.TakerGets,
                        "TakerPays": offer.TakerPays,
                    },
                )
                if trade_offer == None:
                    continue

                trade_offers.append(trade_offer)

    parsed_transaction = {
        "transaction": tx,
        "metadata": metadata,
        "offers": trade_offers,
        "previous_txn_id": previous_txn_hash,
        "date": tx["date"] if "date" in tx else posix_to_ripple_time(0),
    }

    return parsed_transaction


#
# Get the most recent Transaction to affect an Order
#
def get_most_recent_tx(
    client: JsonRpcClient,
    id: OrderId,
    # This is to prevent us spending forever searching through an account's Transactions for an Order
    search_limit: int = DEFAULT_SEARCH_LIMIT,
) -> Any or None:
    order_status = OrderStatus.Open

    ledger_offer_response = client.request(
        LedgerEntry.from_dict(
            {
                "offer": {"account": id.account, "seq": id.sequence},
                "ledger_index": "validated",
            }
        )
    )
    ledger_offer = ledger_offer_response.result

    if "error" not in ledger_offer:
        tx_response = client.request(
            Tx.from_dict({"transaction": ledger_offer["node"]["PreviousTxnID"]})
        )
        tx = tx_response.result

        if tx == None:
            print("No Transaction data!")
            return
        if "error" in tx:
            print("Error: " + tx["error"]["error_message"])
            return

        previous_txn_data = parse_transaction(id, tx)

        if previous_txn_data != None:
            return {
                "previous_txn_data": previous_txn_data,
                "previous_txn_id": previous_txn_data["previous_txn_id"],
                "order_status": order_status,
            }
    elif ledger_offer["error"] != "entryNotFound":
        raise Exception(ledger_offer["error"] + " " + ledger_offer["error_message"])
    else:
        order_status = OrderStatus.Closed

        limit = DEFAULT_LIMIT
        marker: Any
        has_next_page = True
        page = 0

        while has_next_page == True:
            account_tx_request = AccountTx.from_dict(
                {
                    "account": id.account,
                    "limit": limit,
                    "ledger_index_max": -1,
                    "ledger_index_min": -1,
                    "ledger_index": "validated",
                }
            )
            account_tx_response = client.request(account_tx_request)
            account_tx = account_tx_response.result

            if account_tx == None:
                return {"order_status": order_status}

            marker = account_tx["marker"] if "marker" in account_tx else None

            transactions = account_tx["transactions"]

            transactions.sort(reverse=True, key=sort_by_date)

            for transaction in transactions:
                previous_txn_data = parse_transaction(id, transaction)
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


__all__ = [
    "set_transaction_flags_to_number",
    "get_amount_currency_code",
    "get_base_amount_key",
    "get_offer_base_value",
    "get_offer_quote_value",
    "get_book_offer_base_value",
    "get_book_offer_quote_value",
    "get_most_recent_tx",
    "get_offer_from_node",
    "get_offer_from_tx",
    "get_order_side",
    "get_order_side_from_offer",
    "get_quote_amount_key",
    "get_taker_or_maker",
    "order_to_json",
    "parse_transaction",
]
