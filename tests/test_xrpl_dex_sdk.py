from typing import Any, Dict
from xrpl.clients import JsonRpcClient
from xrpl.utils import xrp_to_drops
from xrpl.wallet import generate_faucet_wallet

from xrpl_dex_sdk import __version__, SDK, SDKParams, models, constants
from xrpl_dex_sdk.utils import hash_offer_id
from .fixtures import responses


test_json_rpc_url = constants.Networks[constants.TESTNET]["json_rpc"]
test_client = JsonRpcClient(test_json_rpc_url)

test_wallet_secret = "shCwGCyy17Ph4JdZ6jTsFssEpS6Fs"
test_currency = "AKT"
test_issuer = "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
test_currency_code = test_currency + "+" + test_issuer

sdk_test_params: SDKParams = {
    "network": constants.TESTNET,
    "client": test_client,
    "wallet_secret": test_wallet_secret,
}


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_hash_offer_id() -> None:
    offer_id_hash_1 = hash_offer_id("rn5umFvUWKXqwrGJSRcV24wz9zZFiG7rsQ", 30419151)
    assert (
        offer_id_hash_1
        == "0D5A1CD41A637B533D123EE3408F898875E0F8FCA743CF98599E347F55D606DC"
    )
    offer_id_hash_2 = hash_offer_id("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z", 31617670)
    assert (
        offer_id_hash_2
        == "29B699A1C221904E43650999C5BA5C3B32E6416E4CA390E64EF4392FFACF4406"
    )


def test_ids() -> None:
    order_id = models.OrderId("rn5umFvUWKXqwrGJSRcV24wz9zZFiG7rsQ", 30419151)
    assert order_id.id == "rn5umFvUWKXqwrGJSRcV24wz9zZFiG7rsQ:30419151"
    trade_id = models.TradeId("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z", 31617670)
    assert trade_id.id == "r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z:31617670"


def test_sdk() -> None:
    sdk = SDK(sdk_test_params)
    assert sdk.client != None
    assert sdk.wallet.classic_address == "rpkeJcxB2y5BeAFyycuWwdTTcR3og2a3SR"


def test_cancel_order() -> None:
    sdk = SDK(
        {
            "json_rpc_url": test_json_rpc_url,
            "client": test_client,
            "wallet": generate_faucet_wallet(test_client),
        }
    )
    symbol = models.MarketSymbol(test_currency_code, "XRP")

    create_result = sdk.create_limit_buy_order(
        symbol=symbol,
        amount=2,
        price=1.6,
    )
    assert create_result != None

    cancel_result = sdk.cancel_order(id=create_result.id)

    assert cancel_result != None
    assert cancel_result.id == create_result.id


def test_create_order() -> None:
    sdk = SDK({"client": test_client, "wallet": generate_faucet_wallet(test_client)})
    symbol = models.MarketSymbol(test_currency_code, "XRP")

    amount = 2
    price = 2

    result = sdk.create_order(
        symbol=symbol,
        side=models.OrderSide.Buy,
        type=models.OrderType.Limit,
        amount=amount,
        price=price,
    )

    assert result != None

    tx = result.info["OfferCreate"]["tx_json"]
    assert tx != None
    assert tx["Account"] == sdk.wallet.classic_address
    assert tx["Flags"] & models.OfferCreateFlags.TF_SELL.value == 0
    assert tx["TakerGets"] == xrp_to_drops(amount * price)
    assert tx["TakerPays"]["currency"] == test_currency
    assert tx["TakerPays"]["issuer"] == test_issuer
    assert float(tx["TakerPays"]["value"]) == amount


def test_create_limit_buy_order() -> None:
    sdk = SDK({"client": test_client, "wallet": generate_faucet_wallet(test_client)})
    symbol = models.MarketSymbol(test_currency_code, "XRP")

    amount = 2
    price = 2

    result = sdk.create_limit_buy_order(
        symbol=symbol,
        amount=amount,
        price=price,
    )
    assert result != None

    tx = result.info["OfferCreate"]["tx_json"]
    assert tx != None
    assert tx["Account"] == sdk.wallet.classic_address
    assert tx["Flags"] & models.OfferCreateFlags.TF_SELL.value == 0
    assert tx["TakerGets"] == xrp_to_drops(amount * price)
    assert tx["TakerPays"]["currency"] == test_currency
    assert tx["TakerPays"]["issuer"] == test_issuer
    assert float(tx["TakerPays"]["value"]) == amount


def test_create_limit_sell_order() -> None:
    sdk = SDK({"client": test_client, "wallet": generate_faucet_wallet(test_client)})
    symbol = models.MarketSymbol(test_currency_code, "XRP")

    amount = 5
    price = 1.5

    result = sdk.create_limit_sell_order(
        symbol=symbol,
        amount=amount,
        price=price,
    )
    assert result != None

    tx = result.info["OfferCreate"]["tx_json"]
    assert tx != None
    assert tx["Account"] == sdk.wallet.classic_address
    assert (
        tx["Flags"] & models.OfferCreateFlags.TF_SELL.value
        == models.OfferCreateFlags.TF_SELL.value
    )
    assert tx["TakerPays"] == xrp_to_drops(amount * price)
    assert tx["TakerGets"]["currency"] == test_currency
    assert tx["TakerGets"]["issuer"] == test_issuer
    assert float(tx["TakerGets"]["value"]) == amount


def test_create_trust_line() -> None:
    sdk = SDK(
        {
            "json_rpc_url": test_json_rpc_url,
            "client": test_client,
            "wallet": generate_faucet_wallet(test_client),
        }
    )
    create_result = sdk.create_trust_line(
        code=models.CurrencyCode(test_currency, test_issuer), limit_amount="1000000"
    )
    assert create_result != None


def test_fetch_balance() -> None:
    sdk = SDK(sdk_test_params)
    result = sdk.fetch_balance()
    assert result != None
    assert "balances" in result
    assert "info" in result
    assert "XRP" in result["balances"]
    assert result["info"]["account_info"]["Account"] == sdk.wallet.classic_address


def test_fetch_order() -> None:
    sdk = SDK(sdk_test_params)
    id = models.OrderId("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z", 31617670)
    # expected_response = responses.fetch_order_responses[id.id]

    result = sdk.fetch_order(id)

    assert result != None
    # for field in expected_response.keys():
    #     assert result.__getattribute__(field) != None
    #     expected_value = expected_response[field]
    #     actual_value = result.__getattribute__(field)
    #     if field == "trades":
    #         for index in range(len(expected_value)):
    #             for trade_field in expected_value[index]:
    #                 expected_trade_value = expected_value[index][trade_field]
    #                 actual_trade_value = actual_value[index].__getattribute__(
    #                     trade_field
    #                 )
    #                 if (
    #                     trade_field == "amount"
    #                     or trade_field == "price"
    #                     or trade_field == "cost"
    #                 ):
    #                     assert float(actual_trade_value) == float(expected_trade_value)
    #                 elif trade_field == "fee":
    #                     for fee_field in expected_trade_value:
    #                         if fee_field == "cost" or fee_field == "rate":
    #                             assert float(actual_trade_value[fee_field]) == float(
    #                                 expected_trade_value[fee_field]
    #                             )
    #                         else:
    #                             assert str(actual_trade_value[fee_field]) == str(
    #                                 expected_trade_value[fee_field]
    #                             )
    #                 elif (
    #                     trade_field == "datetime"
    #                     or trade_field == "timestamp"
    #                     or trade_field == "lastTradeTimestamp"
    #                     or trade_field == "info"
    #                 ):
    #                     continue
    #                 elif trade_field == "takerOrMaker":
    #                     assert actual_trade_value == expected_trade_value
    #                 else:
    #                     assert str(actual_trade_value) == str(expected_trade_value)
    #     elif field == "fee":
    #         for fee_field in expected_value:
    #             if fee_field == "cost" or fee_field == "rate":
    #                 assert float(actual_value[fee_field]) == float(
    #                     expected_value[fee_field]
    #                 )
    #             else:
    #                 assert str(actual_value[fee_field]) == str(
    #                     expected_value[fee_field]
    #                 )
    #     elif (
    #         field == "amount"
    #         or field == "price"
    #         or field == "average"
    #         or field == "filled"
    #         or field == "remaining"
    #         or field == "cost"
    #     ):
    #         assert float(actual_value) == float(expected_value)
    #     elif (
    #         field == "datetime"
    #         or field == "timestamp"
    #         or field == "lastTradeTimestamp"
    #         or field == "info"
    #     ):
    #         continue
    #     else:
    #         assert str(actual_value) == str(expected_value)


def test_fetch_orders() -> None:
    sdk = SDK(sdk_test_params)
    # id = models.OrderId("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z", 31617670)
    symbol = models.MarketSymbol(
        "EUR+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP",
        "USD+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP",
    )
    # expected_responses = [responses.fetch_order_responses[id.id]]

    result = sdk.fetch_orders(
        symbol, None, 1, models.FetchOrdersParams(search_limit=25)
    )

    assert result != None
    # assert len(result) > 0
    # for expected_response in expected_responses:
    #     for field in expected_response.keys():
    #         assert result.__getattribute__(field) != None
    #         expected_value = expected_response[field]
    #         actual_value = result.__getattribute__(field)
    #         if field == "trades":
    #             for index in range(len(expected_value)):
    #                 for trade_field in expected_value[index]:
    #                     expected_trade_value = expected_value[index][trade_field]
    #                     actual_trade_value = actual_value[index].__getattribute__(trade_field)
    #                     if (
    #                         trade_field == "amount"
    #                         or trade_field == "price"
    #                         or trade_field == "cost"
    #                     ):
    #                         assert float(actual_trade_value) == float(expected_trade_value)
    #                     elif trade_field == "fee":
    #                         for fee_field in expected_trade_value:
    #                             if fee_field == "cost" or fee_field == "rate":
    #                                 assert float(actual_trade_value[fee_field]) == float(
    #                                     expected_trade_value[fee_field]
    #                                 )
    #                             else:
    #                                 assert str(actual_trade_value[fee_field]) == str(
    #                                     expected_trade_value[fee_field]
    #                                 )
    #                     elif (
    #                         trade_field == "datetime"
    #                         or trade_field == "timestamp"
    #                         or trade_field == "lastTradeTimestamp"
    #                         or trade_field == "info"
    #                     ):
    #                         continue
    #                     elif trade_field == "takerOrMaker":
    #                         assert actual_trade_value == expected_trade_value
    #                     else:
    #                         assert str(actual_trade_value) == str(expected_trade_value)
    #         elif field == "fee":
    #             for fee_field in expected_value:
    #                 if fee_field == "cost" or fee_field == "rate":
    #                     assert float(actual_value[fee_field]) == float(expected_value[fee_field])
    #                 else:
    #                     assert str(actual_value[fee_field]) == str(expected_value[fee_field])
    #         elif (
    #             field == "amount"
    #             or field == "price"
    #             or field == "average"
    #             or field == "filled"
    #             or field == "remaining"
    #             or field == "cost"
    #         ):
    #             assert float(actual_value) == float(expected_value)
    #         elif (
    #             field == "datetime"
    #             or field == "timestamp"
    #             or field == "lastTradeTimestamp"
    #             or field == "info"
    #         ):
    #             continue
    #         else:
    #             assert str(actual_value) == str(expected_value)


def test_fetch_open_orders() -> None:
    sdk = SDK(sdk_test_params)
    symbol = models.MarketSymbol(
        "EUR+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP",
        "USD+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP",
    )

    result = sdk.fetch_open_orders(
        symbol, None, 1, models.FetchOpenOrdersParams(search_limit=25)
    )

    assert result != None


def test_fetch_closed_orders() -> None:
    sdk = SDK(sdk_test_params)
    symbol = models.MarketSymbol(
        "EUR+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP",
        "USD+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP",
    )

    result = sdk.fetch_closed_orders(
        symbol, None, 1, models.FetchClosedOrdersParams(search_limit=25)
    )

    assert result != None


def test_fetch_canceled_orders() -> None:
    sdk = SDK(sdk_test_params)
    symbol = models.MarketSymbol(
        "EUR+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP",
        "USD+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP",
    )

    result = sdk.fetch_canceled_orders(
        symbol, None, 1, models.FetchCanceledOrdersParams(search_limit=25)
    )

    assert result != None


def test_fetch_currencies() -> None:
    sdk = SDK({"network": constants.MAINNET, "wallet_secret": test_wallet_secret})
    currencies = sdk.fetch_currencies()
    assert currencies != None
    assert currencies == responses.fetch_currencies_response


def test_fetch_fees() -> None:
    sdk = SDK(sdk_test_params)
    result = sdk.fetch_fees()
    assert "transactions" in result
    transactions = result["transactions"]
    assert "code" in transactions[0]
    assert "current" in transactions[0]
    assert "transfer" in transactions[0]
    assert "info" in transactions[0]
    trading = result["trading"]
    assert "symbol" in trading[0]
    assert "base" in trading[0]
    assert "quote" in trading[0]
    assert "percentage" in trading[0]
    assert "info" in trading[0]


def test_fetch_issuers() -> None:
    sdk = SDK({"network": constants.MAINNET, "wallet_secret": test_wallet_secret})
    issuers = sdk.fetch_issuers()
    print("issuers")
    print(issuers)
    assert issuers != None
    # assert issuers == responses.fetch_issuers_response


def test_fetch_l2_order_book() -> None:
    sdk = SDK(sdk_test_params)
    test_limit = 3
    test_symbol = models.MarketSymbol("AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP")
    order_book: models.OrderBook = sdk.fetch_l2_order_book(
        symbol=test_symbol,
        limit=test_limit,
        params=models.FetchL2OrderBookParams(taker=sdk.wallet.classic_address),
    )
    expected_order_book = responses.fetch_order_book_response[test_symbol.symbol]
    assert order_book.symbol == expected_order_book["symbol"]
    assert order_book.level == models.OrderBookLevel.L2
    assert order_book.nonce == expected_order_book["nonce"]
    assert order_book.bids == expected_order_book["bids"]
    assert order_book.asks == expected_order_book["asks"]
    assert len(order_book.bids) + len(order_book.asks) == test_limit


def test_fetch_market() -> None:
    sdk = SDK({"network": constants.MAINNET, "wallet_secret": test_wallet_secret})
    market = sdk.fetch_market(
        models.MarketSymbol(
            "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/XRP"
        )
    )
    print("market")
    print(market)
    assert market != None
    # assert markets == responses.fetch_markets_response


def test_fetch_markets() -> None:
    sdk = SDK({"network": constants.MAINNET, "wallet_secret": test_wallet_secret})
    markets = sdk.fetch_markets()
    print("markets")
    print(markets)
    assert markets != None
    # assert markets == responses.fetch_markets_response


def test_fetch_order_book() -> None:
    sdk = SDK(sdk_test_params)
    test_limit = 3
    test_symbol = models.MarketSymbol("AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP")
    order_book: models.OrderBook = sdk.fetch_order_book(
        symbol=test_symbol,
        limit=test_limit,
        params=models.FetchOrderBookParams(taker=sdk.wallet.classic_address),
    )

    expected_order_book = responses.fetch_order_book_response[test_symbol.symbol]
    assert order_book.symbol == expected_order_book["symbol"]
    assert order_book.nonce == expected_order_book["nonce"]
    assert order_book.bids == expected_order_book["bids"]
    assert order_book.asks == expected_order_book["asks"]
    assert len(order_book.bids) + len(order_book.asks) == test_limit


def test_fetch_order_books() -> None:
    sdk = SDK(sdk_test_params)
    test_limit = 3
    test_symbol = models.MarketSymbol("AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP")
    order_books: models.OrderBooks = sdk.fetch_order_books(
        symbols=[test_symbol],
        limit=test_limit,
        params=models.FetchOrderBooksParams(
            symbols={
                test_symbol.symbol: models.FetchOrderBookParams(
                    taker=sdk.wallet.classic_address
                )
            },
        ),
    )

    assert str(test_symbol) in order_books
    order_book_1 = order_books[str(test_symbol)]

    expected_order_book = responses.fetch_order_book_response[str(test_symbol)]
    assert order_book_1.symbol == expected_order_book["symbol"]
    assert order_book_1.nonce == expected_order_book["nonce"]
    assert order_book_1.bids == expected_order_book["bids"]
    assert order_book_1.asks == expected_order_book["asks"]
    assert len(order_book_1.bids) + len(order_book_1.asks) == test_limit


def test_fetch_status() -> None:
    sdk = SDK(sdk_test_params)
    status = sdk.fetch_status()
    assert status != None


def test_fetch_trading_fee() -> None:
    sdk = SDK(sdk_test_params)
    test_symbol = models.MarketSymbol("XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B")
    trading_fee = sdk.fetch_trading_fee(test_symbol)
    assert "symbol" in trading_fee
    assert str(trading_fee["symbol"]) == "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
    assert "base" in trading_fee
    assert trading_fee["base"] == 0
    assert "quote" in trading_fee
    assert trading_fee["quote"] == 0.005
    assert "percentage" in trading_fee
    assert trading_fee["percentage"] == True


def test_fetch_trading_fees() -> None:
    sdk = SDK(sdk_test_params)
    trading_fees = sdk.fetch_trading_fees()

    assert len(trading_fees) == 2

    def sort_fees(fees: Dict[str, Any]):
        return fees["symbol"]

    trading_fees.sort(reverse=False, key=sort_fees)

    trading_fee_1 = trading_fees[0]
    trading_fee_2 = trading_fees[1]

    assert "symbol" in trading_fee_1
    assert str(trading_fee_1["symbol"]) == "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP"
    assert "base" in trading_fee_1
    assert trading_fee_1["base"] == 0.005
    assert "quote" in trading_fee_1
    assert trading_fee_1["quote"] == 0
    assert "percentage" in trading_fee_1
    assert trading_fee_1["percentage"] == True

    assert "symbol" in trading_fee_2
    assert str(trading_fee_2["symbol"]) == "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
    assert "base" in trading_fee_2
    assert trading_fee_2["base"] == 0
    assert "quote" in trading_fee_2
    assert trading_fee_2["quote"] == 0.005
    assert "percentage" in trading_fee_2
    assert trading_fee_2["percentage"] == True


def test_fetch_transaction_fee() -> None:
    sdk = SDK(sdk_test_params)
    transaction_fee = sdk.fetch_transaction_fee(
        "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
    )
    assert "code" in transaction_fee
    assert "current" in transaction_fee
    assert "transfer" in transaction_fee
    assert "info" in transaction_fee


def test_fetch_transaction_fees() -> None:
    sdk = SDK(sdk_test_params)
    transaction_fees = sdk.fetch_transaction_fees(
        ["AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"]
    )
    assert "code" in transaction_fees[0]
    assert transaction_fees[0]["code"] == "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
    assert "current" in transaction_fees[0]
    assert "info" in transaction_fees[0]
    assert "transfer" in transaction_fees[0]


def test_fetch_ticker() -> None:
    sdk = SDK(sdk_test_params)
    ticker = sdk.fetch_ticker("TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP")
    assert ticker != None


def test_fetch_tickers() -> None:
    sdk = SDK(sdk_test_params)
    ticker = sdk.fetch_tickers(["TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP"])
    assert ticker != None
    assert len(ticker) == 1


def test_fetch_trades() -> None:
    sdk = SDK(sdk_test_params)
    base_currency = "EUR+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"
    quote_currency = "CSC+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"
    symbol = base_currency + "/" + quote_currency
    trades = sdk.fetch_trades(
        symbol=symbol, limit=1, params=models.FetchTradesParams(search_limit=100)
    )
    assert trades != None
    # TODO: mock up these responses (too hard to find a real testnet pair with recent trades)
    # assert len(trades) > 0


def test_fetch_my_trades() -> None:
    sdk = SDK(sdk_test_params)
    # TODO: mock up this response
    my_trades = sdk.fetch_my_trades(
        symbol="XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B", limit=3
    )
    assert my_trades != None
    assert len(my_trades) == 3
