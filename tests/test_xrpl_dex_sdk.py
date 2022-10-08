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

sdk_test_params: SDKParams = {
    "client": test_client,
    "wallet_secret": test_wallet_secret,
}


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_hash_offer_id() -> None:
    offer_id_hash_1 = hash_offer_id("rn5umFvUWKXqwrGJSRcV24wz9zZFiG7rsQ", 30419151)
    assert offer_id_hash_1 == "0D5A1CD41A637B533D123EE3408F898875E0F8FCA743CF98599E347F55D606DC"
    offer_id_hash_2 = hash_offer_id("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z", 31617670)
    assert offer_id_hash_2 == "29B699A1C221904E43650999C5BA5C3B32E6416E4CA390E64EF4392FFACF4406"


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
    symbol = models.MarketSymbol(
        models.CurrencyCode(test_currency, test_issuer),
        models.CurrencyCode("XRP"),
    )

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
    symbol = models.MarketSymbol(
        models.CurrencyCode(test_currency, test_issuer),
        models.CurrencyCode("XRP"),
    )

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
    symbol = models.MarketSymbol(
        models.CurrencyCode(test_currency, test_issuer),
        models.CurrencyCode("XRP"),
    )

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
    symbol = models.MarketSymbol(
        models.CurrencyCode("XRP"),
        models.CurrencyCode(test_currency, test_issuer),
    )

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
        tx["Flags"] & models.OfferCreateFlags.TF_SELL.value == models.OfferCreateFlags.TF_SELL.value
    )
    assert tx["TakerGets"] == xrp_to_drops(amount)
    assert tx["TakerPays"]["currency"] == test_currency
    assert tx["TakerPays"]["issuer"] == test_issuer
    assert float(tx["TakerPays"]["value"]) == amount * price


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
        models.CurrencyCode("EUR", "rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
        models.CurrencyCode("USD", "rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
    )
    # expected_responses = [responses.fetch_order_responses[id.id]]

    result = sdk.fetch_orders(symbol, None, 1, models.FetchOrdersParams(search_limit=25))

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
        models.CurrencyCode("EUR", "rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
        models.CurrencyCode("USD", "rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
    )

    result = sdk.fetch_open_orders(symbol, None, 1, models.FetchOpenOrdersParams(search_limit=25))

    assert result != None


def test_fetch_closed_orders() -> None:
    sdk = SDK(sdk_test_params)
    symbol = models.MarketSymbol(
        models.CurrencyCode("EUR", "rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
        models.CurrencyCode("USD", "rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
    )

    result = sdk.fetch_closed_orders(
        symbol, None, 1, models.FetchClosedOrdersParams(search_limit=25)
    )

    assert result != None


def test_fetch_canceled_orders() -> None:
    sdk = SDK(sdk_test_params)
    symbol = models.MarketSymbol(
        models.CurrencyCode("EUR", "rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
        models.CurrencyCode("USD", "rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
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


def test_fetch_issuers() -> None:
    sdk = SDK({"network": constants.MAINNET, "wallet_secret": test_wallet_secret})
    issuers = sdk.fetch_issuers()
    print("issuers")
    print(issuers)
    assert issuers != None
    # assert issuers == responses.fetch_issuers_response


def test_fetch_market() -> None:
    sdk = SDK({"network": constants.MAINNET, "wallet_secret": test_wallet_secret})
    market = sdk.fetch_market(
        models.MarketSymbol(
            models.CurrencyCode(
                "534F4C4F00000000000000000000000000000000",
                "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
            ),
            models.CurrencyCode("XRP"),
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


# def test_fetch_order_book() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.MAINNET)
#     result = client.fetch_order_book(
#         "XRP/USD",
#         3,
#         {
#             "taker": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
#             "taker_pays_issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#         },
#     )
#     assert "symbol" in result
#     assert "nonce" in result
#     assert "bids" in result
#     assert "asks" in result


# def test_fetch_order_books() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.MAINNET)
#     result = client.fetch_order_books(
#         ["XRP/USD"],
#         3,
#         {
#             "XRP/USD": {
#                 "taker": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
#                 "taker_pays_issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#             },
#         },
#     )
#     assert "XRP/USD" in result
#     result_1: Any = result.get("XRP/USD")
#     assert "symbol" in result_1
#     assert "nonce" in result_1
#     assert "bids" in result_1
#     assert "asks" in result_1


def test_fetch_status() -> None:
    sdk = SDK(sdk_test_params)
    status = sdk.fetch_status()
    assert status != None


# def test_fetch_trading_fee() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
#     result = client.fetch_trading_fee("XRP/USD")
#     assert "symbol" in result
#     assert result.get("symbol") == "XRP/USD"
#     assert "base" in result
#     assert result.get("base") == 0
#     assert "quote" in result
#     assert result.get("quote") == 0
#     assert "percentage" in result
#     assert result.get("percentage") == True


# def test_fetch_trading_fees() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
#     result = client.fetch_trading_fees()
#     assert len(result) == 17
#     result_1 = result[0]
#     assert "symbol" in result_1
#     assert result_1.get("symbol") == "534F4C4F00000000000000000000000000000000/XRP"
#     assert "base" in result_1
#     assert result_1.get("base") == 0
#     assert "quote" in result_1
#     assert result_1.get("quote") == 0
#     assert "percentage" in result_1
#     assert result_1.get("percentage") == True


# def test_fetch_transaction_fee() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.MAINNET)
#     result = client.fetch_transaction_fee("EUR")
#     assert "code" in result
#     assert "current" in result
#     assert "info" in result
#     assert "transfer" in result


# def test_fetch_transaction_fees() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.MAINNET)
#     result = client.fetch_transaction_fees(["EUR", "USD"])
#     assert "code" in result[0]
#     assert result[0].get("code") == "EUR"
#     assert "current" in result[0]
#     assert "info" in result[0]
#     assert "transfer" in result[0]
#     assert "code" in result[1]
#     assert result[1].get("code") == "USD"
#     assert "current" in result[1]
#     assert "info" in result[1]
#     assert "transfer" in result[1]


# def test_fetch_fees() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.MAINNET)
#     result = client.fetch_fees()
#     assert "transactions" in result
#     transactions: Any = result.get("transactions")
#     assert "code" in transactions[0]
#     assert "current" in transactions[0]
#     assert "transfer" in transactions[0]
#     assert "info" in transactions[0]
#     trading: Any = result.get("trading")
#     assert "symbol" in trading[0]
#     assert "base" in trading[0]
#     assert "quote" in trading[0]
#     assert "percentage" in trading[0]
#     assert "info" in trading[0]
