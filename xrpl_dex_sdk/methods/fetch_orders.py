from typing import Any, Dict, List, Optional

from xrpl.models.requests.ledger import Ledger
from xrpl.utils import ripple_time_to_posix

from ..constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT
from ..models import (
    FetchOrdersParams,
    FetchOrdersResponse,
    OfferCreateFlags,
    Order,
    OrderId,
    OrderStatus,
    OrderSide,
    MarketSymbol,
    UnixTimestamp,
)
from ..utils import (
    has_offer_create_flag,
    get_quote_amount_key,
    get_base_amount_key,
    get_market_symbol,
)


async def fetch_orders(
    self,
    symbol: Optional[MarketSymbol] = None,
    since: Optional[UnixTimestamp] = None,
    limit: Optional[int] = DEFAULT_LIMIT,
    params: FetchOrdersParams = FetchOrdersParams(),
) -> FetchOrdersResponse:
    orders: List[Order] = []

    has_next_page = True
    previous_ledger_hash: str = None
    tx_count = int(0)

    while has_next_page == True:
        ledger_request = Ledger.from_dict(
            {
                "transactions": True,
                "expand": True,
                "ledger_hash": previous_ledger_hash
                if previous_ledger_hash != None
                else None,
                "ledger_index": "validated" if previous_ledger_hash == None else None,
            }
        )
        ledger_response = await self.client.request(ledger_request)
        ledger_result = ledger_response.result

        if "error" in ledger_result:
            raise Exception("Error: " + ledger_result["error_message"])
            return

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
            if tx_count >= params.search_limit:
                break

            if (
                "Sequence" not in transaction
                or "metaData" not in transaction
                or (
                    transaction["TransactionType"] != "OfferCancel"
                    and transaction["TransactionType"] != "OfferCreate"
                )
            ):
                continue

            if symbol:
                tx_symbol: str = None
                if transaction["TransactionType"] == "OfferCancel":
                    for affected_node in transaction["metaData"]["AffectedNodes"]:
                        if "DeletedNode" in affected_node:
                            node = affected_node["DeletedNode"]
                            if node["LedgerEntryType"] != "Offer":
                                continue
                            if (
                                node["FinalFields"]["Account"] == transaction["Account"]
                                and node["FinalFields"]["Sequence"]
                                == transaction["OfferSequence"]
                            ):
                                tx_symbol = get_market_symbol(node["FinalFields"])
                                break
                else:
                    tx_symbol = get_market_symbol(transaction)
                if tx_symbol != symbol:
                    continue

            order_id = OrderId(transaction["Account"], transaction["Sequence"])

            order = await self.fetch_order(order_id)

            if order == None:
                continue

            if (
                order["status"] == OrderStatus.Open.value
                and params.show_open == False
                or order["status"] == OrderStatus.Closed.value
                and params.show_closed == False
                or order["status"] == OrderStatus.Canceled.value
                and params.show_canceled == False
            ):
                continue

            orders.append(order)

            if len(orders) >= limit:
                break

        has_next_page = len(orders) < limit and tx_count < params.search_limit

    return orders
