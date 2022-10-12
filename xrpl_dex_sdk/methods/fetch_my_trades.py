from typing import Any, Optional

from xrpl.models.requests.account_tx import AccountTx
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime, ripple_time_to_posix

from ..constants import CURRENCY_PRECISION, DEFAULT_LIMIT
from ..models import (
    FetchTradesParams,
    FetchTradesResponse,
    Trade,
    OrderId,
    TradeId,
    TradeType,
    Trade,
    Trades,
    Offer,
    OrderSide,
    TradeType,
    MarketSymbol,
    UnixTimestamp,
)
from ..utils import (
    get_base_amount_key,
    get_quote_amount_key,
    handle_error,
    get_order_side,
    parse_amount_value,
    fetch_transfer_rate,
    get_taker_or_maker,
    get_market_symbol,
    get_amount_currency_code,
)


def fetch_my_trades(
    self,
    # Market symbol to fetch trades for
    symbol: MarketSymbol,
    # Only return Trades since this date
    since: Optional[UnixTimestamp] = None,
    # Total number of Trades to return
    limit: Optional[int] = DEFAULT_LIMIT,
    # eslint-disable-next-line
    params: FetchTradesParams = FetchTradesParams(),
) -> FetchTradesResponse:
    symbol = MarketSymbol(symbol) if isinstance(symbol, str) == True else symbol

    trades: Trades = []

    tx_count = 0
    has_next_page = True
    marker: Any = None

    while has_next_page == True:
        account_tx_response = self.client.request(
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
        handle_error(account_tx_result)

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

            side = get_order_side(tx["Flags"])

            market_symbol = get_market_symbol(
                tx[get_base_amount_key(OrderSide.Buy)]
                if side == OrderSide.Buy
                else tx[get_base_amount_key(OrderSide.Sell)],
                tx[get_quote_amount_key(OrderSide.Buy)]
                if side == OrderSide.Buy
                else tx[get_quote_amount_key(OrderSide.Sell)],
            )

            if market_symbol != symbol:
                continue

            for affected_node in transaction["meta"]["AffectedNodes"]:
                node = (
                    affected_node["ModifiedNode"]
                    if "ModifiedNode" in affected_node
                    else affected_node["DeletedNode"]
                    if "DeletedNode" in affected_node
                    else None
                )

                if node == None or node["LedgerEntryType"] != "Offer" or "FinalFields" not in node:
                    continue

                offer: Offer = node["FinalFields"]

                base_amount = offer[get_base_amount_key(side)]
                base_currency = get_amount_currency_code(base_amount)
                base_rate = fetch_transfer_rate(self.client, base_currency)
                base_amount_value = parse_amount_value(base_amount)
                base_value = (
                    float(drops_to_xrp(str(base_amount_value)))
                    if base_currency == "XRP"
                    else base_amount_value
                )
                if base_value == 0:
                    continue

                quote_amount = offer[get_quote_amount_key(side)]
                quote_currency = get_amount_currency_code(quote_amount)
                quote_rate = fetch_transfer_rate(self.client, quote_currency)
                quote_amount_value = parse_amount_value(quote_amount)
                quote_value = (
                    float(drops_to_xrp(str(quote_amount_value)))
                    if quote_currency == "XRP"
                    else quote_amount_value
                )
                if quote_value == 0:
                    continue

                amount = base_value
                price = quote_value / amount
                cost = amount * price

                fee_rate = quote_rate if side == OrderSide.Buy else base_rate
                fee_cost = (quote_value if side == OrderSide.Buy else base_value) * fee_rate

                trade = Trade(
                    id=TradeId(tx["Account"], tx["Sequence"]),
                    order=OrderId(offer["Account"], offer["Sequence"]),
                    datetime=ripple_time_to_datetime(tx["date"] or 0),
                    timestamp=ripple_time_to_posix(tx["date"] or 0),
                    symbol=MarketSymbol(base_currency.code, quote_currency.code).symbol,
                    type=TradeType.Limit.value,
                    side=side,
                    amount=round(amount, CURRENCY_PRECISION),
                    price=round(price, CURRENCY_PRECISION),
                    takerOrMaker=get_taker_or_maker(side).value,
                    cost=round(cost, CURRENCY_PRECISION),
                    fee={
                        "currency": str(base_currency if side == OrderSide.Buy else quote_currency),
                        "cost": round(fee_cost, CURRENCY_PRECISION),
                        "rate": round(fee_rate, CURRENCY_PRECISION),
                        "percentage": True,
                    }
                    if fee_cost > 0
                    else None,
                    info={"transaction": transaction},
                )

                trades.append(trade)

                if len(trades) >= limit:
                    break

            tx_count += 1
            if tx_count >= params.search_limit:
                break

        has_next_page = len(trades) < limit and tx_count < params.search_limit

    if len(trades) > 0:

        def sort_by_timestamp(trade: Trade):
            return trade.order.sequence

        trades.sort(reverse=False, key=sort_by_timestamp)

    return trades
