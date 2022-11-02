from typing import List, Optional

from xrpl.models.requests.ledger import Ledger
from xrpl.utils import ripple_time_to_posix

from ..constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT
from ..models import (
    FetchOrdersParams,
    FetchOrdersResponse,
    Order,
    OrderId,
    OrderStatus,
    MarketSymbol,
    UnixTimestamp,
)
from ..utils import (
    handle_response_error,
    get_market_symbol,
)


async def fetch_orders(
    self,
    symbol: Optional[MarketSymbol] = None,
    since: Optional[UnixTimestamp] = None,
    limit: int = DEFAULT_LIMIT,
    params: FetchOrdersParams = FetchOrdersParams(),
) -> FetchOrdersResponse:
    """
    Fetches a list of Orders from the dEX.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        (Optional) Symbol to filter Orders by
    since : int
        (Optional) Only return Orders since this date
    limit : int
        (Optional) Total number of Orders to return (default is 20)
    params : xrpl_dex_sdk.models.FetchOrdersParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchOrdersResponse
        The matching Orders
    """

    search_limit = params.search_limit if params.search_limit != None else DEFAULT_SEARCH_LIMIT
    orders: List[Order] = []

    has_next_page = True
    previous_ledger_hash: Optional[str] = None
    tx_count = int(0)

    while has_next_page == True:
        ledger_request = Ledger.from_dict(
            {
                "transactions": True,
                "expand": True,
                "ledger_hash": previous_ledger_hash if previous_ledger_hash != None else None,
                "ledger_index": "validated" if previous_ledger_hash == None else None,
            }
        )
        ledger_response = await self.client.request(ledger_request)
        ledger_result = ledger_response.result
        handle_response_error(ledger_result)

        ledger = ledger_result["ledger"]

        if since != None and ripple_time_to_posix(ledger["close_time"]) < since:
            has_next_page = False
            continue

        previous_ledger_hash = ledger["parent_hash"]

        transactions = ledger["transactions"]

        if transactions == None:
            continue

        for transaction in transactions:
            tx_count += 1
            if len(orders) >= limit or tx_count >= search_limit:
                break

            if (
                isinstance(transaction, str)
                or "Sequence" not in transaction
                or "metaData" not in transaction
                or (
                    transaction["TransactionType"] != "OfferCancel"
                    and transaction["TransactionType"] != "OfferCreate"
                )
            ):
                continue

            if symbol:
                tx_symbol: Optional[MarketSymbol] = None
                if transaction["TransactionType"] == "OfferCancel":
                    for affected_node in transaction["metaData"]["AffectedNodes"]:
                        if "DeletedNode" in affected_node:
                            node = affected_node["DeletedNode"]
                            if node["LedgerEntryType"] != "Offer":
                                continue
                            if (
                                node["FinalFields"]["Account"] == transaction["Account"]
                                and node["FinalFields"]["Sequence"] == transaction["OfferSequence"]
                            ):
                                tx_symbol = get_market_symbol(node["FinalFields"])
                                break
                else:
                    tx_symbol = get_market_symbol(transaction)
                if tx_symbol != symbol:
                    continue

            order_id = OrderId(transaction["Account"], transaction["Sequence"])

            order: Optional[Order] = await self.fetch_order(order_id)

            if order == None:
                continue

            if (
                order.status == OrderStatus.Open
                and params.show_open == False
                or order.status == OrderStatus.Closed
                and params.show_closed == False
                or order.status == OrderStatus.Canceled
                and params.show_canceled == False
            ):
                continue

            orders.append(order)

        has_next_page = len(orders) < limit and tx_count < search_limit

    return orders
