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
    MarketSymbol,
    UnixTimestamp,
)
from ..utils import (
    handle_response_error,
    get_offer_from_node,
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
    """
    Fetch all Trades for a given market symbol.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        (Optional) Market symbol to filter Trades by
    since : int
        (Optional) Only return Trades since this date
    limit : int
        (Optional) Total number of Trades to return (default is 20)
    params : xrpl_dex_sdk.models.FetchTradesParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchTradesResponse
        List of retrieved Trades
    """

    limit = limit if limit != None else DEFAULT_LIMIT
    search_limit = params.search_limit if params.search_limit != None else DEFAULT_SEARCH_LIMIT

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
        ledger_result = ledger_response.result
        handle_response_error(ledger_result)

        ledger = ledger_result["ledger"]

        if since and ripple_time_to_posix(ledger["close_time"] >= since):
            has_next_page = False
            continue

        previous_ledger_hash = ledger["parent_hash"]

        transactions = ledger["transactions"]

        for transaction in transactions:
            tx_count += 1
            if len(trades) >= limit or tx_count >= search_limit:
                break

            if (
                isinstance(transaction, str)
                or "Sequence" not in transaction
                or "metaData" not in transaction
                or transaction["TransactionType"] != "OfferCreate"
                or get_market_symbol(transaction) != symbol
            ):
                continue

            for affected_node in transaction["metaData"]["AffectedNodes"]:
                offer = get_offer_from_node(affected_node)

                if not offer:
                    continue

                trade = await get_trade_from_data(
                    self,
                    {
                        "date": ledger["close_time"],
                        "Flags": offer["Flags"],
                        "OrderAccount": offer["Account"],
                        "OrderSequence": offer["Sequence"],
                        "Account": transaction["Account"],
                        "Sequence": transaction["Sequence"],
                        "TakerPays": offer["TakerPays"],
                        "TakerGets": offer["TakerGets"],
                    },
                    {"transaction": transaction},
                )

                if trade != None:
                    trades.append(trade)

        has_next_page = len(trades) < limit and tx_count < search_limit

    if len(trades) > 0:

        def sort_by_timestamp(trade: Trade):
            return trade.timestamp

        trades.sort(reverse=False, key=sort_by_timestamp)

    return trades
