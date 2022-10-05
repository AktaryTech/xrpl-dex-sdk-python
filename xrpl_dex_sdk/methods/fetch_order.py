from typing import Any, Dict, List, Optional

from xrpl.models.requests.tx import Tx
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime, ripple_time_to_posix

from ..constants import DEFAULT_SEARCH_LIMIT
from ..models.methods.fetch_order import FetchOrderParams, FetchOrderResponse
from ..models.xrpl.offers import OfferCreateFlags, OfferFlags
from ..models.ccxt.orders import Order, OrderId, OrderStatus, OrderSide, OrderTimeInForce, OrderType
from ..models.ccxt.trades import Trade, TradeSide, TradeType
from ..models import CurrencyCode, MarketSymbol
from ..utils.fees import fetch_transfer_rate
from ..utils.hashes import hash_offer_id
from ..utils.orders import get_most_recent_tx, parse_transaction, get_taker_or_maker


def fetch_order(
    self,
    id: OrderId,
    symbol: Optional[MarketSymbol] = None,
    params: FetchOrderParams = {"search_limit": DEFAULT_SEARCH_LIMIT},
) -> FetchOrderResponse:

    transactions: List[Any] = []

    previous_txn = get_most_recent_tx(self.client, id, params["search_limit"])
    print("previous_txn")
    print(previous_txn)

    if previous_txn == None:
        return

    order_status = previous_txn["order_status"] or OrderStatus.Open
    previous_txn_id = previous_txn["previous_txn_id"]
    previous_txn_data = previous_txn["previous_txn_data"]
    if previous_txn_data != None:
        transactions.append(previous_txn_data)

    while previous_txn_id != None:
        tx_request = Tx.from_dict({"transaction": previous_txn_id, "ledger_index": "validated"})
        tx_response = self.json_rpc(tx_request)
        previous_txn_data = parse_transaction(id, tx_response)
        if previous_txn_data != None:
            transactions.append(previous_txn_data["previous_txn_id"])

    trades: List[Trade] = []
    order: Order or None
    filled: float = 0
    fill_price: float = 0
    total_fill_price: float = fill_price

    for transaction_data in transactions:
        transaction, offers, date = transaction_data

        for offer in offers:
            source = offer

            if "Sequence" not in source:
                return

            side: TradeSide = (
                "sell" if (source.Flags & OfferFlags.LSF_SELL) == OfferFlags.LSF_SELL else "buy"
            )

            base_amount = source.TakerPays if side == "buy" else source.TakerGets
            base_code = (
                CurrencyCode("XRP")
                if base_amount == str
                else CurrencyCode(base_amount["currency"], base_amount["issuer"])
            )
            base_value = float(
                drops_to_xrp(base_amount) if base_amount == str else base_amount["value"]
            )

            quote_amount = source.TakerGets if side == "buy" else source.TakerPays
            quote_code = (
                CurrencyCode("XRP")
                if quote_amount == str
                else CurrencyCode(quote_amount["currency"], quote_amount["issuer"])
            )
            quote_rate = fetch_transfer_rate(self.client, quote_amount)
            quote_value = (
                float(drops_to_xrp(quote_amount)) if quote_amount == str else quote_amount["value"]
            )

            amount = base_value
            price = quote_value / amount
            cost = amount * price

            fee_rate = quote_rate
            fee_cost = quote_value * fee_rate

            filled = filled + amount
            fill_price = price
            total_fill_price = total_fill_price + fill_price

            trade: Trade = {
                "id": OrderId(source.Account, source.Sequence),
                "order": id,
                "datetime": ripple_time_to_datetime(date or 0),
                "timestamp": ripple_time_to_posix(date or 0),
                "symbol": MarketSymbol(base_code, quote_code),
                "type": TradeType.Limit,
                "side": side,
                "amount": amount,
                "price": price,
                "takerOrMaker": get_taker_or_maker(side),
                "cost": cost,
                "info": {"offer": offer, "transaction": transaction},
            }

            if fee_cost > 0:
                trade.fee = {
                    "currency": str(quote_code),
                    "cost": fee_cost,
                    "rate": fee_rate,
                    "percentage": True,
                }

            trades.append(trade)

        if transaction["Account"] == id.account and transaction["Sequence"] == id.sequence:
            source = transaction

            if "Sequence" not in source:
                return

            side: OrderSide = (
                "sell"
                if (source.Flags & OfferCreateFlags.TF_SELL) == OfferCreateFlags.TF_SELL
                else "buy"
            )

            base_amount = source.TakerPays if side == "buy" else source.TakerGets
            base_code = (
                CurrencyCode("XRP")
                if base_amount == str
                else CurrencyCode(base_amount["currency"], base_amount["issuer"])
            )
            base_value = float(
                drops_to_xrp(base_amount) if base_amount == str else base_amount["value"]
            )

            quote_amount = source.TakerGets if side == "buy" else source.TakerPays
            quote_code = (
                CurrencyCode("XRP")
                if quote_amount == str
                else CurrencyCode(quote_amount["currency"], quote_amount["issuer"])
            )
            quote_rate = fetch_transfer_rate(self.client, quote_amount)
            quote_value = (
                float(drops_to_xrp(quote_amount)) if quote_amount == str else quote_amount["value"]
            )

            order_time_in_force: OrderTimeInForce = OrderTimeInForce.GoodTillCanceled
            if source.Flags == OfferCreateFlags.TF_PASSIVE:
                order_time_in_force = OrderTimeInForce.PostOnly
            elif source.Flags == OfferCreateFlags.TF_FILL_OR_KILL:
                order_time_in_force = OrderTimeInForce.FillOrKill
            elif source.Flags == OfferCreateFlags.TF_IMMEDIATE_OR_CANCEL:
                order_time_in_force = OrderTimeInForce.ImmediateOrCancel

            amount = base_value
            price = quote_value / amount
            actual_price = fill_price
            average = total_fill_price / len(trades) if len(trades) > 0 else float(0)
            remaining = amount - filled
            cost = filled * actual_price

            fee_rate = quote_rate
            fee_cost = filled * fee_rate

            order = {
                "id": OrderId(source.Account, source.Sequence),
                "clientOrderId": hash_offer_id(source.Account, source.Sequence),
                "order": id,
                "datetime": ripple_time_to_datetime(date or 0),
                "timestamp": ripple_time_to_posix(date or 0),
                "lastTradeTimestamp": ripple_time_to_posix(transactions[0].date or 0),
                "status": order_status,
                "symbol": MarketSymbol(base_code, quote_code),
                "type": OrderType.Limit,
                "timeInForce": order_time_in_force,
                "side": side,
                "amount": amount,
                "price": price,
                "average": average,
                "filled": filled,
                "remaining": remaining,
                "cost": cost,
                "trades": trades,
                "info": {"transaction": transaction},
            }

            if fee_cost > 0:
                trade.fee = {
                    "currency": str(quote_code),
                    "cost": fee_cost,
                    "rate": fee_rate,
                    "percentage": True,
                }

    return order
