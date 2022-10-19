from typing import Any, Dict, Optional

from xrpl.models.requests.ledger import Ledger
from xrpl.utils import ripple_time_to_posix

from ..constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT
from ..models import (
    FetchTradesParams,
    FetchTradesResponse,
    Trade,
    Trade,
    Trades,
    Offer,
    MarketSymbol,
    UnixTimestamp,
)
from ..utils import (
    handle_response_error,
    parse_affected_node,
    get_market_symbol,
    get_trade_from_data,
)


async def fetch_trades(
    self,
    # Market symbol to fetch trades for
    symbol: MarketSymbol,
    # Only return Trades since this date
    since: Optional[UnixTimestamp] = None,
    # Total number of Trades to return
    limit: Optional[int] = None,
    # eslint-disable-next-line
    params: FetchTradesParams = FetchTradesParams(),
) -> FetchTradesResponse:
    limit = limit if limit != None else DEFAULT_LIMIT
    search_limit = (
        params.search_limit if params.search_limit != None else DEFAULT_SEARCH_LIMIT
    )

    trades: Trades = []

    tx_count = 0
    has_next_page = True
    previous_ledger_hash: Optional[str] = None

    while has_next_page == True:
        ledger_request: Dict[str, Any] = {"transactions": True, "expand": True}
        if previous_ledger_hash != None:
            ledger_request["ledger_hash"] = previous_ledger_hash
        else:
            ledger_request["ledger_index"] = "validated"

        ledger_response = await self.client.request(Ledger.from_dict(ledger_request))
        ledger = ledger_response.result
        handle_response_error(ledger)

        if since != None and ripple_time_to_posix(
            ledger["ledger"]["close_time"] >= since
        ):
            has_next_page = False
            continue

        previous_ledger_hash = ledger["ledger"]["parent_hash"]

        transactions = ledger["ledger"]["transactions"]

        for transaction in transactions:
            if (
                "Sequence" not in transaction
                or "metaData" not in transaction
                or transaction["TransactionType"] != "OfferCreate"
                or get_market_symbol(transaction) != symbol
            ):
                continue

            for affected_node in transaction["metaData"]["AffectedNodes"]:
                node = parse_affected_node(affected_node)
                if node == None:
                    continue

                offer_fields = getattr(node, "FinalFields")
                if offer_fields == None:
                    continue

                trade = await get_trade_from_data(
                    self,
                    {
                        "date": ledger["ledger"]["close_time"],
                        "Flags": offer_fields["Flags"],
                        "OrderAccount": offer_fields["Account"],
                        "OrderSequence": offer_fields["Sequence"],
                        "Account": transaction["Account"],
                        "Sequence": transaction["Sequence"],
                        "TakerPays": offer_fields["TakerPays"],
                        "TakerGets": offer_fields["TakerGets"],
                    },
                    {"transaction": transaction},
                )

                if trade != None:
                    trades.append(trade)
                    if len(trades) >= limit:
                        break

            tx_count += 1
            if tx_count >= search_limit:
                break

        has_next_page = len(trades) < limit and tx_count < search_limit

    if len(trades) > 0:

        def sort_by_timestamp(trade: Trade):
            return trade.timestamp

        sorted_trades = trades.sort(reverse=False, key=sort_by_timestamp)
        if sorted_trades != None:
            trades = sorted_trades

    return trades
