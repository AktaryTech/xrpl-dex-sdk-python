from typing import Any, Optional

from xrpl.models.requests.account_tx import AccountTx
from xrpl.utils import ripple_time_to_posix

from ..constants import DEFAULT_LIMIT, DEFAULT_SEARCH_LIMIT
from ..models import (
    FetchMyTradesParams,
    FetchMyTradesResponse,
    Trade,
    Trade,
    Trades,
    MarketSymbol,
    UnixTimestamp,
)
from ..utils import (
    handle_response_error,
    get_market_symbol,
    get_trade_from_data,
    get_offer_from_node,
)


async def fetch_my_trades(
    self,
    symbol: MarketSymbol,
    since: Optional[UnixTimestamp] = None,
    limit: Optional[int] = None,
    params: FetchMyTradesParams = FetchMyTradesParams(),
) -> FetchMyTradesResponse:
    """
    Fetch the SDK user's Trades for a given market symbol

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        (Optional) Market symbol to filter Trades by
    since : int
        (Optional) Only return Trades since this date
    limit : int
        (Optional) Total number of Trades to return (default is 20)
    params : xrpl_dex_sdk.models.FetchMyTradesParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchMyTradesResponse
        List of retrieved Trades
    """

    limit = limit if limit != None else DEFAULT_LIMIT
    search_limit = params.search_limit if params.search_limit != None else DEFAULT_SEARCH_LIMIT

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

        if "marker" in account_tx_result:
            marker = account_tx_result["marker"]

        if account_tx_result["validated"] == False:
            continue

        transactions = account_tx_result["transactions"]

        if transactions == None:
            continue

        for transaction in transactions:
            tx_count += 1
            if len(trades) >= limit or tx_count >= search_limit:
                break

            if "tx" not in transaction:
                continue

            tx = transaction["tx"]

            if (
                "Sequence" not in tx
                or isinstance(transaction["meta"], str)
                or tx["TransactionType"] != "OfferCreate"
                or not tx["date"]
                or get_market_symbol(tx) != symbol
            ):
                continue

            if since != None and ripple_time_to_posix(tx["date"]) >= since:
                has_next_page = False
                continue

            for affected_node in transaction["meta"]["AffectedNodes"]:
                offer = get_offer_from_node(affected_node)

                if not offer:
                    continue

                trade = await get_trade_from_data(
                    self,
                    {
                        "date": tx["date"],
                        "Flags": offer["Flags"],
                        "OrderAccount": offer["Account"],
                        "OrderSequence": offer["Sequence"],
                        "Account": tx["Account"],
                        "Sequence": tx["Sequence"],
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
