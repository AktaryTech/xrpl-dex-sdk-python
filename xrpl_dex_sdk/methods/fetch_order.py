from typing import Any, List, Optional

from xrpl.models.requests.tx import Tx

from ..constants import DEFAULT_SEARCH_LIMIT
from ..models import (
    FetchOrderParams,
    FetchOrderResponse,
    Order,
    OrderId,
    OrderStatus,
    Trade,
    Offer,
    MarketSymbol,
    UnixTimestamp,
)
from ..utils import (
    get_most_recent_tx,
    parse_transaction,
    sort_by_date,
    get_trade_from_data,
    get_order_from_data,
)


async def fetch_order(
    self,
    id: OrderId,
    symbol: Optional[MarketSymbol] = None,
    params: FetchOrderParams = {"search_limit": DEFAULT_SEARCH_LIMIT},
) -> FetchOrderResponse:
    transactions: List[Any] = []

    previous_txn = await get_most_recent_tx(self.client, id, params["search_limit"])

    if previous_txn == None:
        print("Could not find previous Transaction! Aborting...")
        return

    order_status = previous_txn["order_status"] or OrderStatus.Open
    previous_txn_id: str or None = previous_txn["previous_txn_id"]
    previous_txn_data = previous_txn["previous_txn_data"]

    if previous_txn_data != None:
        transactions.append(previous_txn_data)

    while previous_txn_id != None:
        tx_response = await self.client.request(
            Tx.from_dict({"transaction": previous_txn_id})
        )
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
        raise Exception("Couldn't find data for OrderId " + str(id))

    transactions.sort(reverse=True, key=sort_by_date)

    for transaction_data in transactions:
        transaction = transaction_data["transaction"]
        offers: List[Offer] = transaction_data["offers"]
        date = transaction_data["date"]

        if last_trade_timestamp == None:
            last_trade_timestamp = date

        for offer in offers:
            source = offer

            if source.Sequence == None:
                continue

            trade = await get_trade_from_data(
                self,
                {
                    "date": date,
                    "Flags": offer.Flags,
                    "OrderAccount": offer.Account,
                    "OrderSequence": offer.Sequence,
                    "Account": id.account,
                    "Sequence": id.sequence,
                    "TakerPays": offer.TakerPays,
                    "TakerGets": offer.TakerGets,
                },
                {"offer": offer},
            )

            if trade != None:
                trades.append(trade)

        if (
            transaction["Account"] == id.account
            and transaction["Sequence"] == id.sequence
        ):
            source = transaction

            if "Sequence" not in source:
                raise Exception("Couldn't find data for OrderId " + str(id))

            order = await get_order_from_data(
                self,
                {
                    "status": order_status,
                    "date": date,
                    "filled": filled,
                    "fill_price": fill_price,
                    "total_fill_price": total_fill_price,
                    "trades": trades,
                    "Flags": transaction["Flags"],
                    "Account": transaction["Account"],
                    "Sequence": transaction["Sequence"],
                    "TakerPays": transaction["TakerPays"],
                    "TakerGets": transaction["TakerGets"],
                },
                {"transaction_data": transaction_data},
            )

    return order
