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
    handle_response_error,
    parse_transaction,
    sort_by_date,
    get_trade_from_data,
    get_order_from_data,
)


async def fetch_order(
    self,
    id: OrderId,
    symbol: Optional[MarketSymbol] = None,
    params: FetchOrderParams = FetchOrderParams(),
) -> Optional[FetchOrderResponse]:
    """
    Fetches an Order from the dEX.

    Parameters
    ----------
    id : xrpl_dex_sdk.models.OrderId
        ID of the Order to fetch
    symbol : xrpl_dex_sdk.models.MarketSymbol
        (Optional) The symbol of the Order to fetch
    params : xrpl_dex_sdk.models.FetchOrderParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchOrderResponse
        The matching Order
    """

    search_limit = params.search_limit if params.search_limit else DEFAULT_SEARCH_LIMIT
    transactions: List[Any] = []

    previous_txn = await get_most_recent_tx(self.client, id, search_limit)

    if previous_txn == None:
        raise Exception("Couldn't find data for OrderId " + str(id))

    order_status = previous_txn["order_status"] or OrderStatus.Open
    previous_txn_id: str or None = previous_txn["previous_txn_id"]
    previous_txn_data = previous_txn["previous_txn_data"]

    if previous_txn_data != None:
        transactions.append(previous_txn_data)

    #
    # Build a Transaction history for this Order
    #
    while previous_txn_id != None:
        tx_response = await self.client.request(Tx.from_dict({"transaction": previous_txn_id}))
        previous_txn_response = tx_response.result
        handle_response_error(previous_txn_response)

        if previous_txn_response:
            previous_txn_data = parse_transaction(id, previous_txn_response)
            if previous_txn_data:
                transactions.append(previous_txn_data)
                previous_txn_id = previous_txn_data["previous_txn_id"]

    if len(transactions) == 0:
        # raise Exception("Couldn't find data for OrderId " + str(id))
        return

    trades: List[Trade] = []
    order: Optional[Order] = None
    last_trade_timestamp: Optional[UnixTimestamp] = None
    filled = float(0)
    fill_price = float(0)
    total_fill_price = float(fill_price)

    # Newest to oldest
    transactions.sort(reverse=True, key=sort_by_date)

    for transaction_data in transactions:
        transaction = transaction_data["transaction"]
        offers: List[Offer] = transaction_data["offers"]
        date = transaction_data["date"]

        for offer in offers:
            source = offer

            if not source.Sequence:
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

            if trade:
                trades.append(trade)
                filled += trade.amount
                fill_price = trade.price
                total_fill_price += fill_price
                if last_trade_timestamp == None:
                    last_trade_timestamp = date

        if id == transaction:
            if "Sequence" not in transaction:
                # raise Exception("Couldn't find data for OrderId " + str(id))
                return

            order = await get_order_from_data(
                self,
                {
                    "status": order_status,
                    "date": date,
                    "last_trade_timestamp": last_trade_timestamp,
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
