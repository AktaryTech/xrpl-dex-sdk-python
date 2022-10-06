from typing import Any, List, Optional

from xrpl.models.requests.tx import Tx
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime, ripple_time_to_posix

from ..constants import DEFAULT_SEARCH_LIMIT
from ..models import (
    FetchOrderParams,
    FetchOrderResponse,
    OfferCreateFlags,
    OfferFlags,
    Order,
    OrderId,
    OrderStatus,
    OrderTimeInForce,
    OrderSide,
    OrderType,
    Trade,
    TradeSide,
    TradeType,
    CurrencyCode,
    MarketSymbol,
    UnixTimestamp,
)
from ..utils import (
    fetch_transfer_rate,
    get_most_recent_tx,
    hash_offer_id,
    has_offer_flag,
    has_offer_create_flag,
    parse_transaction,
    get_taker_or_maker,
    sort_by_date,
    parse_amount_value,
)


def fetch_order(
    self,
    id: OrderId,
    symbol: Optional[MarketSymbol] = None,
    params: FetchOrderParams = {"search_limit": DEFAULT_SEARCH_LIMIT},
) -> FetchOrderResponse:

    print("Getting Order: " + id.id)

    transactions: List[Any] = []

    previous_txn = get_most_recent_tx(self.client, id, params["search_limit"])

    if previous_txn == None:
        print("Could not find previous Transaction! Aborting...")
        return

    order_status = previous_txn["order_status"] or OrderStatus.Open
    previous_txn_id: str or None = previous_txn["previous_txn_id"]
    previous_txn_data = previous_txn["previous_txn_data"]

    if previous_txn_data != None:
        transactions.append(previous_txn_data)

    while previous_txn_id != None:
        tx_response = self.client.request(Tx.from_dict({"transaction": previous_txn_id}))
        tx = tx_response.result

        if "error" in tx:
            print("Error: " + tx["error_message"])
            return

        previous_txn_data = parse_transaction(id, tx)

        if previous_txn_data != None:
            transactions.append(previous_txn_data)
            previous_txn_id = previous_txn_data["previous_txn_id"]

    trades: List[Trade] = []
    order: Order or None = None
    last_trade_timestamp: UnixTimestamp or None = None
    filled: float = 0
    fill_price: float = 0
    total_fill_price: float = fill_price

    if len(transactions) == 0:
        print("Could not find any Transactions for this Order! Aborting...")
        return

    print("Preparing to loop through " + str(len(transactions)) + " Transactions")

    transactions.sort(reverse=True, key=sort_by_date)

    for transaction_data in transactions:
        transaction = transaction_data["transaction"]
        offers = transaction_data["offers"]
        date = transaction_data["date"]

        if last_trade_timestamp == None:
            last_trade_timestamp = date

        for offer in offers:
            source = offer

            if source.Sequence == None:
                print("Could not find Sequence property in Offer! Aborting...")
                return

            side: TradeSide = (
                TradeSide.Sell.value
                if has_offer_flag(source.Flags, OfferFlags.LSF_SELL)
                else TradeSide.Buy.value
            )

            base_amount = source.TakerPays if side == TradeSide.Buy.value else source.TakerGets
            base_code = (
                CurrencyCode(base_amount["currency"], base_amount["issuer"])
                if "currency" in base_amount
                else CurrencyCode("XRP")
            )
            base_amount_value = parse_amount_value(base_amount)
            base_value = (
                float(drops_to_xrp(str(base_amount_value)))
                if isinstance(base_amount_value, int)
                else base_amount_value
            )

            quote_amount = source.TakerGets if side == TradeSide.Buy.value else source.TakerPays
            quote_code = (
                CurrencyCode(quote_amount["currency"], quote_amount["issuer"])
                if "currency" in quote_amount
                else CurrencyCode("XRP")
            )
            quote_rate = fetch_transfer_rate(self.client, quote_amount)
            quote_amount_value = parse_amount_value(quote_amount)
            quote_value = (
                float(drops_to_xrp(str(quote_amount_value)))
                if isinstance(quote_amount_value, int)
                else quote_amount_value
            )

            amount = base_value
            price = quote_value / amount
            cost = amount * price

            fee_rate = quote_rate
            fee_cost = quote_value * fee_rate

            filled = filled + amount
            fill_price = price
            total_fill_price = total_fill_price + fill_price

            trade = Trade(
                id=OrderId(source.Account, source.Sequence),
                order=id,
                datetime=ripple_time_to_datetime(date or 0),
                timestamp=ripple_time_to_posix(date or 0),
                symbol=MarketSymbol(base_code, quote_code),
                type=TradeType.Limit,
                side=side,
                amount=amount,
                price=price,
                takerOrMaker=get_taker_or_maker(side),
                cost=cost,
                fee={
                    "currency": str(quote_code),
                    "cost": fee_cost,
                    "rate": fee_rate,
                    "percentage": True,
                }
                if fee_cost > 0
                else None,
                info={"offer": offer, "transaction": transaction},
            )

            trades.append(trade)

        if transaction["Account"] == id.account and transaction["Sequence"] == id.sequence:
            source = transaction

            if "Sequence" not in source:
                print("Could not find Sequence property in Transaction! Aborting...")
                return

            side: OrderSide = (
                OrderSide.Sell.value
                if has_offer_create_flag(source["Flags"], OfferCreateFlags.TF_SELL)
                else OrderSide.Buy.value
            )

            base_amount = (
                source["TakerPays"] if side == OrderSide.Buy.value else source["TakerGets"]
            )
            base_code = (
                CurrencyCode("XRP")
                if isinstance(base_amount, str)
                else CurrencyCode(base_amount["currency"], base_amount["issuer"])
            )
            base_amount_value = parse_amount_value(base_amount)
            base_value = (
                float(drops_to_xrp(str(base_amount_value)))
                if isinstance(base_amount_value, int)
                else base_amount_value
            )

            quote_amount = (
                source["TakerGets"] if side == OrderSide.Buy.value else source["TakerPays"]
            )
            quote_code = (
                CurrencyCode("XRP")
                if isinstance(quote_amount, str)
                else CurrencyCode(quote_amount["currency"], quote_amount["issuer"])
            )
            quote_rate = fetch_transfer_rate(self.client, quote_amount)
            quote_amount_value = parse_amount_value(quote_amount)
            quote_value = (
                float(drops_to_xrp(str(quote_amount_value)))
                if isinstance(quote_amount_value, int)
                else quote_amount_value
            )

            order_time_in_force: OrderTimeInForce = OrderTimeInForce.GoodTillCanceled.value
            if (
                source["Flags"] & OfferCreateFlags.TF_PASSIVE.value
            ) == OfferCreateFlags.TF_PASSIVE.value:
                order_time_in_force = OrderTimeInForce.PostOnly.value
            elif (
                source["Flags"] & OfferCreateFlags.TF_FILL_OR_KILL.value
            ) == OfferCreateFlags.TF_FILL_OR_KILL.value:
                order_time_in_force = OrderTimeInForce.FillOrKill.value
            elif (
                source["Flags"] & OfferCreateFlags.TF_IMMEDIATE_OR_CANCEL.value
            ) == OfferCreateFlags.TF_IMMEDIATE_OR_CANCEL.value:
                order_time_in_force = OrderTimeInForce.ImmediateOrCancel.value

            amount = base_value
            price = quote_value / amount
            actual_price = fill_price
            average = total_fill_price / len(trades) if len(trades) > 0 else float(0)
            remaining = amount - filled
            cost = filled * actual_price

            fee_rate = quote_rate
            fee_cost = filled * fee_rate

            order = Order(
                id=OrderId(source["Account"], source["Sequence"]),
                clientOrderId=hash_offer_id(source["Account"], source["Sequence"]),
                datetime=ripple_time_to_datetime(date or 0),
                timestamp=ripple_time_to_posix(date or 0),
                lastTradeTimestamp=last_trade_timestamp
                if last_trade_timestamp != None
                else ripple_time_to_posix(0),
                status=order_status,
                symbol=MarketSymbol(base_code, quote_code),
                type=OrderType.Limit,
                timeInForce=order_time_in_force,
                side=side,
                amount=amount,
                price=price,
                average=average,
                filled=filled,
                remaining=remaining,
                cost=cost,
                trades=trades,
                fee={
                    "currency": str(quote_code),
                    "cost": fee_cost,
                    "rate": fee_rate,
                    "percentage": True,
                }
                if fee_cost > 0
                else None,
                info={"transaction": transaction},
            )

    return order
