import json
from typing import Any, Dict, List, NamedTuple, Optional, Union

from xrpl.clients import JsonRpcClient
from xrpl.models.requests.ledger_entry import LedgerEntry
from xrpl.models.requests.tx import Tx
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.requests.account_tx import AccountTx
from xrpl.utils import (
    posix_to_ripple_time,
    drops_to_xrp,
    ripple_time_to_datetime,
    ripple_time_to_posix,
)


from ..constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT, CURRENCY_PRECISION
from ..models import (
    Amount,
    LedgerEntryTypes,
    CurrencyCode,
    OrderId,
    OrderSide,
    OrderStatus,
    TradeTakerOrMaker,
    TradeSide,
    Offer,
    MarketSymbol,
    Trade,
    OrderTimeInForce,
    OfferCreateFlags,
    OfferFlags,
    Node,
    TransactionMetadata,
)

from .numbers import subtract_amounts, parse_amount_value
from .data import omit, sort_by_date
from .hashes import hash_offer_id


def parse_affected_node(
    affected_node: Node, entry_type: Optional[LedgerEntryTypes] = LedgerEntryTypes.Offer
):
    parsed_node = (
        affected_node["CreatedNode"]
        if "CreatedNode" in affected_node
        else affected_node["ModifiedNode"]
        if "ModifiedNode" in affected_node
        else affected_node["DeletedNode"]
        if "DeletedNode" in affected_node
        else None
    )

    return (
        parsed_node
        if parsed_node != None and parsed_node["LedgerEntryType"] == entry_type.value
        else None
    )


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


def get_order_time_in_force(input: Dict[str, Any]) -> OrderTimeInForce:
    order_time_in_force: OrderTimeInForce = OrderTimeInForce.GoodTillCanceled.value
    if (
        input["Flags"] & OfferCreateFlags.TF_PASSIVE.value
    ) == OfferCreateFlags.TF_PASSIVE.value:
        order_time_in_force = OrderTimeInForce.PostOnly.value
    elif (
        input["Flags"] & OfferCreateFlags.TF_FILL_OR_KILL.value
    ) == OfferCreateFlags.TF_FILL_OR_KILL.value:
        order_time_in_force = OrderTimeInForce.FillOrKill.value
    elif (
        input["Flags"] & OfferCreateFlags.TF_IMMEDIATE_OR_CANCEL.value
    ) == OfferCreateFlags.TF_IMMEDIATE_OR_CANCEL.value:
        order_time_in_force = OrderTimeInForce.ImmediateOrCancel.value
    return order_time_in_force


def get_taker_or_maker(side: TradeSide) -> TradeTakerOrMaker:
    return (
        TradeTakerOrMaker.Maker if side == TradeSide.Sell else TradeTakerOrMaker.Taker
    )


def get_order_side_from_flags(flags: int) -> OrderSide:
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


def get_base_amount_key(side: OrderSide or TradeSide) -> str:
    return (
        "TakerPays" if (side == OrderSide.Buy or side == TradeSide.Buy) else "TakerGets"
    )


def get_quote_amount_key(side: OrderSide or TradeSide) -> str:
    return (
        "TakerGets" if (side == OrderSide.Buy or side == TradeSide.Buy) else "TakerPays"
    )


def get_amount_currency_code(amount: Amount) -> CurrencyCode:
    return "XRP" if isinstance(amount, str) else amount["currency"]


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
# Get Base and Quote Currency data
# @param source Offer | Transaction
# @returns Data object with Base/Quote information
#
def get_base_and_quote_data(source: Dict[str, Any]):
    data: Dict[str, Any] = {}

    data["side"] = get_order_side_from_flags(source["Flags"])
    data["base_amount"] = source[get_base_amount_key(data["side"])]
    base_amount_value = parse_amount_value(data["base_amount"])
    data["base_value"] = (
        float(drops_to_xrp(str(base_amount_value)))
        if isinstance(base_amount_value, int)
        else base_amount_value
    )
    if data["base_value"] == float(0):
        return

    data["quote_amount"] = source[get_quote_amount_key(data["side"])]
    quote_amount_value = parse_amount_value(data["quote_amount"])
    data["quote_value"] = (
        float(drops_to_xrp(str(quote_amount_value)))
        if isinstance(quote_amount_value, int)
        else quote_amount_value
    )
    if data["quote_value"] == float(0):
        return

    data["symbol"] = MarketSymbol(
        get_amount_currency_code(
            data["base_amount"]["currency"]
            if "currency" in data["base_amount"]
            else data["base_amount"]
        ),
        get_amount_currency_code(
            data["quote_amount"]["currency"]
            if "currency" in data["quote_amount"]
            else data["quote_amount"]
        ),
    )

    return data


#
# Get Base and Quote Currency data
# @param source Offer | Transaction
# @returns Data object with Base/Quote information
#
async def get_shared_order_data(sdk, source: Dict[str, Any]):
    data: Dict[str, Any] = get_base_and_quote_data(source)
    if data == None:
        return

    data["base_currency"] = get_amount_currency_code(data["base_amount"])
    data["base_issuer"] = (
        data["base_amount"]["issuer"] if "issuer" in data["base_amount"] else None
    )
    data["base_rate"] = (
        await sdk.fetch_transfer_rate(data["base_issuer"])
        if data["base_issuer"] != None
        else 0
    )

    data["quote_currency"] = get_amount_currency_code(data["quote_amount"])
    data["quote_issuer"] = (
        data["quote_amount"]["issuer"] if "issuer" in data["quote_amount"] else None
    )
    data["quote_rate"] = (
        await sdk.fetch_transfer_rate(data["quote_issuer"])
        if data["quote_issuer"] != None
        else 0
    )

    data["amount"] = data["base_value"]
    data["price"] = data["quote_value"] / data["base_value"]

    data["fee_currency"] = (
        data["quote_currency"]
        if data["side"] == OrderSide.Buy
        else data["base_currency"]
    )
    data["fee_rate"] = (
        data["quote_rate"] if data["side"] == OrderSide.Buy else data["base_rate"]
    )

    return data


#
# Get Order fee from source data
#
def get_order_fee_from_data(fee_cost: float, source: Dict[str, Any]):
    return (
        {
            "currency": str(source["quote_currency"]),
            "cost": round(fee_cost, CURRENCY_PRECISION),
            "rate": round(source["fee_rate"], CURRENCY_PRECISION),
            "percentage": True,
        }
        if fee_cost > 0
        else None
    )


#
# Parse OrderSourceData into a CCXT Order object
# @param this SDKContext
# @param source OrderSourceData
# @param info Record<string, any>
# @returns Order
#
async def get_order_from_data(
    sdk, input_data: Dict[str, Any], info: Dict[str, Any] = {}
):
    source_data = await get_shared_order_data(sdk, input_data)
    if source_data == None:
        return
    data = {**input_data, **source_data}

    actual_price = data["fill_price"]
    average: float = (
        data["total_fill_price"] / len(data["trades"]) if len(data["trades"]) > 0 else 0
    )
    remaining = data["amount"] - data["filled"]
    cost = data["filled"] * actual_price

    order = {
        "id": OrderId(data["Account"], data["Sequence"]),
        "client_order_id": hash_offer_id(data["Account"], data["Sequence"]),
        "datetime": ripple_time_to_datetime(data["date"]).isoformat(),
        "timestamp": ripple_time_to_posix(data["date"]),
        "status": data["status"],
        "symbol": data["symbol"],
        "type": "limit",
        "timeInForce": get_order_time_in_force(data),
        "side": data["side"],
        "amount": round(data["amount"], CURRENCY_PRECISION),
        "price": round(data["price"], CURRENCY_PRECISION),
        "average": round(average, CURRENCY_PRECISION),
        "filled": round(data["filled"], CURRENCY_PRECISION),
        "remaining": round(remaining, CURRENCY_PRECISION),
        "cost": round(cost, CURRENCY_PRECISION),
        "trades": data["trades"],
        "info": info,
    }

    if len(data["trades"]):
        order["last_trade_timestamp"] = data["trades"][-1]["timestamp"]

    fee_cost = data["filled"] * data["fee_rate"]
    fee = get_order_fee_from_data(fee_cost, data)
    if fee:
        order["fee"] = fee

    return order


#
# Parse TradeSourceData into a CCXT Trade object
# @param this SDKContext
# @param source TradeSourceData
# @param info Record<string, any>
# @returns Trade
#
async def get_trade_from_data(
    sdk, input_data: Dict[str, Any], info: Dict[str, Any] = {}
):
    source_data = await get_shared_order_data(sdk, input_data)
    if source_data == None:
        return
    data = {**input_data, **source_data}

    trade_id = OrderId(data["Account"], data["Sequence"])
    order_id = OrderId(data["OrderAccount"], data["OrderSequence"])

    cost = data["amount"] * data["price"]

    trade: Trade = {
        "id": trade_id,
        "order": order_id,
        "datetime": ripple_time_to_datetime(data["date"] or 0).isoformat(),
        "timestamp": ripple_time_to_posix(data["date"] or 0),
        "symbol": data["symbol"],
        "type": "limit",
        "side": data["side"],
        "amount": round(data["amount"], CURRENCY_PRECISION),
        "price": round(data["price"], CURRENCY_PRECISION),
        "taker_or_maker": get_taker_or_maker(data["side"]),
        "cost": round(cost, CURRENCY_PRECISION),
        "info": info,
    }

    fee_cost = (
        data["quote_value"] if data["side"] == OrderSide.Buy else data["base_value"]
    ) * data["fee_rate"]
    fee = get_order_fee_from_data(fee_cost, data)
    if fee:
        trade["fee"] = fee

    return trade


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
async def get_most_recent_tx(
    client: JsonRpcClient,
    id: OrderId,
    # This is to prevent us spending forever searching through an account's Transactions for an Order
    search_limit: int = DEFAULT_SEARCH_LIMIT,
) -> Any or None:
    order_status = OrderStatus.Open

    ledger_offer_response = await client.request(
        LedgerEntry.from_dict(
            {
                "offer": {"account": id.account, "seq": id.sequence},
                "ledger_index": "validated",
            }
        )
    )
    ledger_offer = ledger_offer_response.result

    if "error" not in ledger_offer:
        tx_response = await client.request(
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
            account_tx_response = await client.request(account_tx_request)
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
    "parse_affected_node",
    "get_amount_currency_code",
    "get_base_amount_key",
    "get_order_from_data",
    "get_trade_from_data",
    "get_offer_base_value",
    "get_order_time_in_force",
    "get_offer_quote_value",
    "get_book_offer_base_value",
    "get_book_offer_quote_value",
    "get_most_recent_tx",
    "get_offer_from_node",
    "get_offer_from_tx",
    "get_order_side_from_flags",
    "get_order_side_from_offer",
    "get_quote_amount_key",
    "get_taker_or_maker",
    "order_to_json",
    "parse_transaction",
]
