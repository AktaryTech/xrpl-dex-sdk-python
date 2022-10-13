from typing import Optional

from xrpl.models.requests.ledger import Ledger
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
    handle_response_error,
    get_order_side,
    parse_amount_value,
    get_taker_or_maker,
    get_amount_currency_code,
)


async def fetch_trades(
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

    sell_base_field = get_base_amount_key(OrderSide.Sell)
    sell_quote_field = get_quote_amount_key(OrderSide.Sell)
    buy_base_field = get_base_amount_key(OrderSide.Buy)
    buy_quote_field = get_quote_amount_key(OrderSide.Buy)

    trades: Trades = []

    tx_count = 0
    has_next_page = True
    previous_ledger_hash: str = None

    while has_next_page == True:
        ledger_request = {"transactions": True, "expand": True}
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
            if "Sequence" not in transaction or "metaData" not in transaction:
                continue

            if transaction["TransactionType"] == "OfferCreate":

                side = get_order_side(transaction["Flags"])

                market_symbol = MarketSymbol(
                    get_amount_currency_code(
                        transaction[buy_base_field]
                        if side == OrderSide.Buy
                        else transaction[sell_base_field]
                    ).code,
                    get_amount_currency_code(
                        transaction[buy_quote_field]
                        if side == OrderSide.Buy
                        else transaction[sell_quote_field]
                    ).code,
                )

                if market_symbol.symbol != symbol.symbol:
                    continue

                for affected_node in transaction["metaData"]["AffectedNodes"]:
                    node = (
                        affected_node["ModifiedNode"]
                        if "ModifiedNode" in affected_node
                        else affected_node["DeletedNode"]
                        if "DeletedNode" in affected_node
                        else None
                    )

                    if (
                        node == None
                        or node["LedgerEntryType"] != "Offer"
                        or "FinalFields" not in node
                    ):
                        continue

                    offer: Offer = node["FinalFields"]

                    base_amount = offer[get_base_amount_key(side)]
                    base_currency = get_amount_currency_code(base_amount)
                    base_amount_value = parse_amount_value(base_amount)
                    base_value = (
                        float(drops_to_xrp(str(base_amount_value)))
                        if isinstance(base_amount_value, int)
                        else base_amount_value
                    )

                    quote_amount = offer[get_quote_amount_key(side)]
                    quote_currency = get_amount_currency_code(quote_currency)
                    quote_rate = (
                        await self.fetch_transfer_rate(quote_currency.issuer)
                        if "issuer" in quote_currency
                        else 0
                    )
                    quote_amount_value = parse_amount_value(quote_amount)
                    quote_value = (
                        float(drops_to_xrp(str(quote_amount_value)))
                        if isinstance(quote_amount_value, int)
                        else quote_amount_value
                    )

                    amount = base_value
                    price = quote_value / amount
                    cost = amount * price

                    fee_rate = quote_rate
                    fee_cost = quote_value * fee_rate

                    filled = filled + amount
                    fill_price = price
                    total_fill_price = total_fill_price + fill_price

                    trade = Trade(
                        id=TradeId(transaction["Account"], transaction["Sequence"]),
                        order=OrderId(offer.Account, offer.Sequence),
                        datetime=ripple_time_to_datetime(
                            ledger["ledger"]["close_time"] or 0
                        ),
                        timestamp=ripple_time_to_posix(
                            ledger["ledger"]["close_time"] or 0
                        ),
                        symbol=MarketSymbol(
                            base_currency.code, quote_currency.code
                        ).symbol,
                        type=TradeType.Limit.value,
                        side=side,
                        amount=round(amount, CURRENCY_PRECISION),
                        price=round(price, CURRENCY_PRECISION),
                        takerOrMaker=get_taker_or_maker(side).value,
                        cost=round(cost, CURRENCY_PRECISION),
                        fee={
                            "currency": str(quote_currency),
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
            return trade["timestamp"]

        trades = trades.sort(reverse=False, key=sort_by_timestamp)

    return trades
