from typing import Any, Dict, List, Optional, Union

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.models.requests.ledger_entry import LedgerEntry
from xrpl.models.requests.tx import Tx

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
    IssuedCurrencyAmount,
    LedgerEntryTypes,
    CurrencyCode,
    OrderId,
    OrderSide,
    BookOffer,
    OrderStatus,
    OrderType,
    Fee,
    TradeTakerOrMaker,
    TradeSide,
    Offer,
    TradeType,
    MarketSymbol,
    TradeId,
    Order,
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
from .errors import handle_response_error


def parse_affected_node(
    affected_node: dict,
    entry_type: Optional[LedgerEntryTypes] = LedgerEntryTypes.Offer,
) -> Optional[Node]:
    """
    Parses a Node and returns its data in an agnostic format.

    Parameters
    ----------
    affected_node : Dict
        Node object to parse
    entry_type : xrpl_dex_sdk.models.LedgerEntryType
        LedgerEntry type to filter by (defaults to Offer)

    Returns
    -------
    xrpl_dex_sdk.models.Node
        The parsed Node, or None if unable to parse.
    """

    entry_type = LedgerEntryTypes.Offer if entry_type == None else entry_type

    if "CreatedNode" in affected_node:
        node_data: Dict[str, Any] = affected_node["CreatedNode"]
        if node_data["LedgerEntryType"] != entry_type.value:
            return
        return Node(
            type="CreatedNode",
            LedgerEntryType=node_data["LedgerEntryType"],
            LedgerIndex=node_data["LedgerIndex"],
            NewFields=node_data["NewFields"],
        )
    elif "ModifiedNode" in affected_node:
        node_data: Dict[str, Any] = affected_node["ModifiedNode"]
        if node_data["LedgerEntryType"] != entry_type.value:
            return
        return Node(
            type="ModifiedNode",
            LedgerEntryType=node_data["LedgerEntryType"],
            LedgerIndex=node_data["LedgerIndex"],
            FinalFields=node_data["FinalFields"] if "FinalFields" in node_data else None,
            PreviousFields=node_data["PreviousFields"] if "PreviousFields" in node_data else None,
            PreviousTxnID=node_data["PreviousTxnID"] if "PreviousTxnID" in node_data else None,
            PreviousTxnLgrSeq=node_data["PreviousTxnLgrSeq"]
            if "PreviousTxnLgrSeq" in node_data
            else None,
        )
    elif "DeletedNode" in affected_node:
        node_data: Dict[str, Any] = affected_node["DeletedNode"]
        if node_data["LedgerEntryType"] != entry_type.value:
            return
        return Node(
            type="DeletedNode",
            LedgerEntryType=node_data["LedgerEntryType"],
            LedgerIndex=node_data["LedgerIndex"],
            FinalFields=node_data["FinalFields"] if "FinalFields" in node_data else None,
            PreviousFields=node_data["PreviousFields"] if "PreviousFields" in node_data else None,
        )


def get_order_time_in_force(input: Dict[str, Any]) -> OrderTimeInForce:
    """Parses an Order and returns its time in force."""

    order_time_in_force: OrderTimeInForce = OrderTimeInForce.GoodTillCanceled
    if (input["Flags"] & OfferCreateFlags.TF_PASSIVE.value) == OfferCreateFlags.TF_PASSIVE.value:
        order_time_in_force = OrderTimeInForce.PostOnly
    elif (
        input["Flags"] & OfferCreateFlags.TF_FILL_OR_KILL.value
    ) == OfferCreateFlags.TF_FILL_OR_KILL.value:
        order_time_in_force = OrderTimeInForce.FillOrKill
    elif (
        input["Flags"] & OfferCreateFlags.TF_IMMEDIATE_OR_CANCEL.value
    ) == OfferCreateFlags.TF_IMMEDIATE_OR_CANCEL.value:
        order_time_in_force = OrderTimeInForce.ImmediateOrCancel
    return order_time_in_force


def get_taker_or_maker(side: TradeSide) -> TradeTakerOrMaker:
    """Gets whether a Trade was from a taker or maker."""

    return TradeTakerOrMaker.Maker if side == TradeSide.Sell else TradeTakerOrMaker.Taker


def get_order_side_from_flags(flags: int) -> OrderSide:
    """Parses an Offer's flags and returns its side (buy or sell)."""

    if flags & OfferFlags.LSF_SELL.value == OfferFlags.LSF_SELL.value:
        return OrderSide.Sell
    elif flags & OfferCreateFlags.TF_SELL.value == OfferCreateFlags.TF_SELL.value:
        return OrderSide.Sell
    else:
        return OrderSide.Buy


def get_amount(source: Union[dict, str]) -> Amount:
    """Creates an Amount from a `CurrencyCode` and value."""

    return (
        source
        if isinstance(source, str)
        else IssuedCurrencyAmount(
            currency=source["currency"],
            issuer=source["issuer"],
            value=source["value"],
        )
    )


def get_market_symbol(source: Dict[str, Any]):
    """Gets a MarketSymbol from an Offer or Transaction."""

    side = get_order_side_from_flags(source["Flags"])
    base_amount = get_amount(source[get_base_amount_key(side)])
    quote_amount = get_amount(source[get_quote_amount_key(side)])
    return get_market_symbol_from_amount(base_amount, quote_amount)


# Gets a MarketSymbol from Base and Quote XRPL Amounts.
# @param base Base currency as Amount object
# @param quote Quote currency as Amount object
# @returns MarketSymbol instance
#
def get_market_symbol_from_amount(base: Amount, quote: Amount) -> MarketSymbol:
    """
    Gets a MarketSymbol from Base and Quote XRPL Amounts.

    Parameters
    ----------
    base : xrpl_dex_sdk.models.Amount
        Base currency as Amount object
    quote : xrpl_dex_sdk.models.Amount
        Quote currency as Amount object

    Returns
    -------
    xrpl_dex_sdk.models.MarketSymbol
    """

    return MarketSymbol(
        CurrencyCode.from_string("XRP")
        if isinstance(base, str)
        else CurrencyCode(base.currency, base.issuer),
        CurrencyCode.from_string("XRP")
        if isinstance(quote, str)
        else CurrencyCode(quote.currency, quote.issuer),
    )


def get_base_amount_key(side: OrderSide or TradeSide) -> str:
    """Gets the Offer object key of the Offer's base currency."""

    return "TakerPays" if (side == OrderSide.Buy or side == TradeSide.Buy) else "TakerGets"


def get_quote_amount_key(side: OrderSide or TradeSide) -> str:
    """Gets the Offer object key of the Offer's quote currency."""

    return "TakerGets" if (side == OrderSide.Buy or side == TradeSide.Buy) else "TakerPays"


def get_amount_currency_code(amount: Amount) -> CurrencyCode:
    """Parses an Amount object and returns the currency code."""

    return (
        CurrencyCode("XRP")
        if isinstance(amount, str)
        else CurrencyCode(amount["currency"])
        if isinstance(amount, dict)
        else CurrencyCode(amount.currency)
    )


def get_book_offer_taker_pays(book_offer: BookOffer):
    """Creates a TakerPays object for a book_offers request."""

    return (
        getattr(book_offer, "taker_pays_funded")
        if getattr(book_offer, "taker_pays_funded") != None
        else book_offer.TakerPays
    )


def get_book_offer_taker_gets(book_offer: BookOffer):
    """Creates a TakerGets object for a book_offers request."""

    return (
        getattr(book_offer, "taker_gets_funded")
        if getattr(book_offer, "taker_gets_funded") != None
        else book_offer.TakerGets
    )


def get_book_offer_base_value(book_offer: BookOffer) -> float:
    """Gets the base currency value from a BookOffer instance."""

    amount = (
        get_book_offer_taker_pays(book_offer)
        if book_offer.Flags & OfferFlags.LSF_SELL.value == 0
        else get_book_offer_taker_gets(book_offer)
    )
    return float(drops_to_xrp(amount) if isinstance(amount, str) else getattr(amount, "value"))


def get_book_offer_quote_value(book_offer: BookOffer) -> float:
    """Gets the quote currency value from a BookOffer instance."""

    quote_amount = (
        get_book_offer_taker_gets(book_offer)
        if book_offer.Flags & OfferFlags.LSF_SELL.value == 0
        else get_book_offer_taker_pays(book_offer)
    )
    return float(
        drops_to_xrp(quote_amount)
        if isinstance(quote_amount, str)
        else getattr(quote_amount, "value")
    )


def get_offer_from_node(node: dict) -> Optional[Offer]:
    """Returns an Offer object from an AffectedNode."""

    affected_node = parse_affected_node(node, LedgerEntryTypes.Offer)

    if affected_node == None or affected_node.FinalFields == None:
        return

    LedgerIndex = affected_node.LedgerIndex
    FinalFields = affected_node.FinalFields
    PreviousTxnID = (
        affected_node.PreviousTxnID
        if affected_node.PreviousTxnID != None
        else FinalFields["PreviousTxnID"]
    )
    PreviousFields = affected_node.PreviousFields if affected_node.PreviousFields != None else None

    offer_index = LedgerIndex

    taker_gets = (
        subtract_amounts(PreviousFields["TakerGets"], FinalFields["TakerGets"])
        if PreviousFields != None
        else FinalFields["TakerGets"]
    )
    taker_pays = (
        subtract_amounts(PreviousFields["TakerPays"], FinalFields["TakerPays"])
        if PreviousFields != None
        else FinalFields["TakerPays"]
    )

    offer = Offer(
        Account=FinalFields["Account"],
        BookDirectory="",
        BookNode="0",
        Flags=FinalFields["Flags"],
        LedgerEntryType=LedgerEntryTypes.Offer,
        OwnerNode="0",
        PreviousTxnID=PreviousTxnID,
        PreviousTxnLgrSeq=0,
        Sequence=FinalFields["Sequence"],
        TakerGets=taker_gets,
        TakerPays=taker_pays,
        index=offer_index,
        Expiration=None,
    )

    return offer


def get_offer_from_tx(
    transaction: Any, overrides: Optional[Dict[str, Any]] = {}
) -> Optional[Offer]:
    """
    Returns an Offer Ledger object from a Transaction.

    Parameters
    ----------
    transaction : Dict
        Transaction to parse
    overrides : Dict
        (Optional) Object of values to override transaction defaults with
    """

    if transaction["TransactionType"] != "OfferCreate":
        return

    Account = (
        overrides["Account"]
        if overrides != None and "Account" in overrides
        else transaction["Account"]
    )
    Flags = (
        overrides["Flags"] if overrides != None and "Flags" in overrides else transaction["Flags"]
    )
    Sequence = (
        overrides["Sequence"]
        if overrides != None and "Sequence" in overrides
        else transaction["Sequence"]
        if "Sequence" in transaction
        else None
    )
    TakerGets = (
        overrides["TakerGets"]
        if overrides != None and "TakerGets" in overrides
        else transaction["TakerGets"]
    )
    TakerPays = (
        overrides["TakerPays"]
        if overrides != None and "TakerPays" in overrides
        else transaction["TakerPays"]
    )
    PreviousTxnID = (
        overrides["PreviousTxnID"] if overrides != None and "PreviousTxnID" in overrides else ""
    )

    if Sequence == None:
        return

    offer = Offer(
        Account=Account,
        BookDirectory="",
        BookNode="0",
        Flags=Flags,
        LedgerEntryType=LedgerEntryTypes.Offer,
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


def get_base_and_quote_data(source: Dict[str, Any]):
    """Get Base and Quote Currency data."""

    data: Dict[str, Any] = {}

    data["side"] = get_order_side_from_flags(source["Flags"])

    data["base_amount"] = source[get_base_amount_key(data["side"])]
    base_amount_value = parse_amount_value(
        IssuedCurrencyAmount(
            currency=data["base_amount"]["currency"],
            issuer=data["base_amount"]["issuer"],
            value=data["base_amount"]["value"],
        )
        if "issuer" in data["base_amount"]
        else data["base_amount"]
    )
    data["base_value"] = (
        float(drops_to_xrp(str(base_amount_value)))
        if isinstance(base_amount_value, int)
        else base_amount_value
    )
    if data["base_value"] == float(0):
        return

    data["quote_amount"] = source[get_quote_amount_key(data["side"])]
    quote_amount_value = parse_amount_value(
        IssuedCurrencyAmount(
            currency=data["quote_amount"]["currency"],
            issuer=data["quote_amount"]["issuer"],
            value=data["quote_amount"]["value"],
        )
        if "issuer" in data["quote_amount"]
        else data["quote_amount"]
    )
    data["quote_value"] = (
        float(drops_to_xrp(str(quote_amount_value)))
        if isinstance(quote_amount_value, int)
        else quote_amount_value
    )
    if data["quote_value"] == float(0):
        return

    data["symbol"] = get_market_symbol(source)

    return data


async def get_shared_order_data(sdk, source: Dict[str, Any]):
    """Get basic Order data."""

    data = get_base_and_quote_data(source)
    if data == None:
        return

    data["base_currency"] = get_amount_currency_code(data["base_amount"])
    data["base_issuer"] = data["base_amount"]["issuer"] if "issuer" in data["base_amount"] else None
    data["base_rate"] = (
        await sdk.fetch_transfer_rate(data["base_issuer"]) if data["base_issuer"] != None else 0
    )

    data["quote_currency"] = get_amount_currency_code(data["quote_amount"])
    data["quote_issuer"] = (
        data["quote_amount"]["issuer"] if "issuer" in data["quote_amount"] else None
    )
    data["quote_rate"] = (
        await sdk.fetch_transfer_rate(data["quote_issuer"]) if data["quote_issuer"] != None else 0
    )

    data["amount"] = data["base_value"]
    data["price"] = data["quote_value"] / data["base_value"]

    data["fee_currency"] = (
        data["quote_currency"] if data["side"] == OrderSide.Buy else data["base_currency"]
    )
    data["fee_rate"] = data["quote_rate"] if data["side"] == OrderSide.Buy else data["base_rate"]

    return data


def get_order_fee_from_data(fee_cost: float, source: Dict[str, Any]) -> Optional[Fee]:
    """Get Order fee from source data."""

    return (
        Fee(
            currency=source["quote_currency"],
            cost=round(fee_cost, CURRENCY_PRECISION),
            rate=round(source["fee_rate"], CURRENCY_PRECISION),
            percentage=True,
        )
        if fee_cost > 0
        else None
    )


async def get_order_from_data(sdk, input_data: Dict[str, Any], info: dict = {}):
    """
    Parse OrderSourceData into a CCXT Order object.

    Parameters
    ----------
    input_data : Dict
        OrderSourceData to parse
    info: Dict
        Info object with raw exchange responses

    Returns
    -------
    xrpl_dex_sdk.models.Order
        The parsed Order
    """

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

    fee_cost = data["filled"] * data["fee_rate"]
    fee = get_order_fee_from_data(fee_cost, data) if fee_cost > 0 else None

    last_trade_timestamp = data["trades"][-1].timestamp if len(data["trades"]) else None

    order = Order(
        id=OrderId(data["Account"], data["Sequence"]),
        client_order_id=hash_offer_id(data["Account"], data["Sequence"]),
        datetime=ripple_time_to_datetime(data["date"]).isoformat(),
        timestamp=ripple_time_to_posix(data["date"]),
        last_trade_timestamp=last_trade_timestamp,
        status=data["status"],
        symbol=data["symbol"],
        type=OrderType.Limit,
        time_in_force=get_order_time_in_force(data),
        side=data["side"],
        amount=round(data["amount"], CURRENCY_PRECISION),
        price=round(data["price"], CURRENCY_PRECISION),
        average=round(average, CURRENCY_PRECISION),
        filled=round(data["filled"], CURRENCY_PRECISION),
        remaining=round(remaining, CURRENCY_PRECISION),
        cost=round(cost, CURRENCY_PRECISION),
        trades=data["trades"],
        fee=fee if fee != None else None,
        info=info,
    )

    return order


async def get_trade_from_data(sdk, input_data: Dict[str, Any], info: dict = {}):
    """
    Parse TradeSourceData into a CCXT Trade object.

    Parameters
    ----------
    input_data : Dict
        TradeSourceData to parse
    info: Dict
        Info object with raw exchange responses

    Returns
    -------
    xrpl_dex_sdk.models.Trade
        The parsed Trade
    """

    source_data = await get_shared_order_data(sdk, input_data)
    if source_data == None:
        return
    data = {**input_data, **source_data}

    trade_id = TradeId(data["Account"], data["Sequence"])
    order_id = OrderId(data["OrderAccount"], data["OrderSequence"])

    cost = data["amount"] * data["price"]

    fee_cost = (
        data["quote_value"] if data["side"] == OrderSide.Buy else data["base_value"]
    ) * data["fee_rate"]

    fee = get_order_fee_from_data(fee_cost, data)

    trade = Trade(
        id=trade_id,
        order=order_id,
        datetime=ripple_time_to_datetime(data["date"] or 0).isoformat(),
        timestamp=ripple_time_to_posix(data["date"] or 0),
        symbol=data["symbol"],
        type=TradeType.Limit,
        side=data["side"],
        amount=round(data["amount"], CURRENCY_PRECISION),
        price=round(data["price"], CURRENCY_PRECISION),
        taker_or_maker=get_taker_or_maker(data["side"]),
        cost=round(cost, CURRENCY_PRECISION),
        fee=fee if fee != None else None,
        info=info,
    )

    return trade


#
# Parse a Transaction and return the important data
#
def parse_transaction(id: OrderId, transaction: Any) -> Optional[Dict[str, Any]]:
    """
    Parse any Transaction and return data relevant to creating an Order/Trade.

    Parameters
    ----------
    order_id : xrpl_dex_sdk.models.OrderId
        ID to filter with when parsing
    transaction : Dict
        Transaction data to parse
    """

    offer_ledger_index = hash_offer_id(id.account, id.sequence)

    previous_txn_hash: Optional[str] = None
    tx: Any = None
    metadata: Optional[TransactionMetadata] = None

    if "result" in transaction:
        if transaction["result"]["TransactionType"] != "OfferCreate":
            return
        tx = transaction["result"]
        metadata = TransactionMetadata(
            AffectedNodes=transaction["meta"]["AffectedNodes"],
            TransactionIndex=transaction["meta"]["TransactionIndex"],
            TransactionResult=transaction["meta"]["TransactionResult"],
            DeliveredAmount=None,
            delivered_amount=None,
        )
    elif "tx" in transaction:
        if transaction["tx"]["TransactionType"] != "OfferCreate":
            return
        tx = transaction["tx"]
        metadata = TransactionMetadata(
            AffectedNodes=transaction["meta"]["AffectedNodes"],
            TransactionIndex=transaction["meta"]["TransactionIndex"],
            TransactionResult=transaction["meta"]["TransactionResult"],
            DeliveredAmount=None,
            delivered_amount=None,
        )
    elif "metaData" in transaction:
        if transaction["TransactionType"] != "OfferCreate":
            return
        tx = omit(transaction, {"metaData"})
        metadata = TransactionMetadata(
            AffectedNodes=transaction["metaData"]["AffectedNodes"],
            TransactionIndex=transaction["metaData"]["TransactionIndex"],
            TransactionResult=transaction["metaData"]["TransactionResult"],
            DeliveredAmount=None,
            delivered_amount=None,
        )
    elif "meta" in transaction:
        if transaction["TransactionType"] != "OfferCreate":
            return
        tx = omit(transaction, {"meta"})
        metadata = transaction["meta"]
        metadata = TransactionMetadata(
            AffectedNodes=transaction["meta"]["AffectedNodes"],
            TransactionIndex=transaction["meta"]["TransactionIndex"],
            TransactionResult=transaction["meta"]["TransactionResult"],
            DeliveredAmount=None,
            delivered_amount=None,
        )

    if tx == None:
        print("Could not get Transaction data! Skipping...")
        return
    elif "hash" not in tx:
        print('Property "hash" not found on Transaction! Skipping...')
        return
    elif metadata == None:
        print("Metadata not found! Skipping...")
        return

    trade_offers: List[Offer] = []

    if id == tx:
        for affected_node in metadata.AffectedNodes:
            offer = get_offer_from_node(affected_node)
            if offer != None and offer.Account != id.account:
                trade_offers.append(offer)
        previous_txn_hash = None
    elif tx["Account"] != id.account:
        for affected_node in metadata.AffectedNodes:
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


async def get_most_recent_tx(
    client: AsyncJsonRpcClient,
    id: OrderId,
    search_limit: int = DEFAULT_SEARCH_LIMIT,
) -> Any or None:
    """
    Get data for the most recent Transaction to affect an Order.

    Parameters
    ----------
    client : xrpl_dex_sdk.clients.AsyncJsonRpcClient
        Client to use when looking up data
    order_id : xrpl_dex_sdk.models.OrderId
        ID to filter with when parsing
    search_limit : int
        Max total transactions to search through looking for matching ones
    """

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
        handle_response_error(tx)

        if tx == None:
            print("No Transaction data!")
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
        marker: Any = None
        has_next_page = True
        page = 0

        while has_next_page == True:
            account_tx_request = AccountTx.from_dict(
                {
                    "account": id.account,
                    "ledger_index_min": -1,
                    "ledger_index_max": -1,
                    "ledger_index": "validated",
                    "limit": limit,
                    "marker": marker,
                }
            )
            account_tx_response = await client.request(account_tx_request)
            account_tx = account_tx_response.result
            handle_response_error(account_tx)

            if account_tx == None:
                return {"order_status": order_status}

            marker = account_tx["marker"] if "marker" in account_tx else None

            transactions = account_tx["transactions"]

            transactions.sort(reverse=True, key=sort_by_date)

            for transaction in transactions:
                if isinstance(transaction["meta"], str):
                    continue

                # Check for canceled offers

                # previous_txn_data = parse_transaction(id, transaction)
                # if previous_txn_data != None:
                #     return {
                #         "previous_txn_data": previous_txn_data,
                #         "previous_txn_id": previous_txn_data["previous_txn_id"],
                #         "order_status": order_status,
                #     }

            if marker == None or limit * page >= search_limit:
                has_next_page = False
            else:
                page += 1
