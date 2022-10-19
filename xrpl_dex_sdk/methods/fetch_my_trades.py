from typing import Any, Optional

from xrpl.models.requests.account_tx import AccountTx
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
    Node,
    UnixTimestamp,
)
from ..utils import (
    handle_response_error,
    get_market_symbol,
    get_trade_from_data,
    parse_affected_node,
)


async def fetch_my_trades(
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
    marker: Any = None

    while has_next_page == True:
        account_tx_response = await self.client.request(
            AccountTx.from_dict(
                {
                    "account": self.wallet.classic_address,
                    "ledger_index_min": -1,
                    "ledger_index_max": -1,
                    "limit": DEFAULT_LIMIT,
                    "marker": marker,
                }
            )
        )
        account_tx_result = account_tx_response.result
        handle_response_error(account_tx_result)

        if account_tx_result["validated"] == False:
            continue

        if "marker" in account_tx_result:
            marker = account_tx_result["marker"]

        transactions = account_tx_result["transactions"]

        if transactions == None:
            continue

        for transaction in transactions:
            if "tx" not in transaction:
                continue

            tx = transaction["tx"]

            if tx["TransactionType"] != "OfferCreate" or "Sequence" not in tx:
                continue

            if since != None and ripple_time_to_posix(tx["date"]) >= since:
                continue

            if get_market_symbol(tx) != symbol:
                continue

            for affected_node in transaction["meta"]["AffectedNodes"]:
                node = parse_affected_node(affected_node)
                if node == None:
                    continue

                offer_fields = getattr(node, "FinalFields")
                if offer_fields == None:
                    continue

                trade = await get_trade_from_data(
                    self,
                    {
                        "date": tx["date"],
                        "Flags": offer_fields["Flags"],
                        "OrderAccount": offer_fields["Account"],
                        "OrderSequence": offer_fields["Sequence"],
                        "Account": tx["Account"],
                        "Sequence": tx["Sequence"],
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

        trades.sort(reverse=False, key=sort_by_timestamp)

    return trades
