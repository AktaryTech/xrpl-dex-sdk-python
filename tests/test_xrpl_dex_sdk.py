from xrpl_dex_sdk import __version__, SDK, SDKParams, models, constants
from xrpl_dex_sdk.utils import hash_offer_id
from .fixtures.responses import fetch_order_responses

sdk_test_params: SDKParams = {
    "network": constants.TESTNET,
    "wallet_secret": "shCwGCyy17Ph4JdZ6jTsFssEpS6Fs",
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
    expected_response = fetch_order_responses[id.id]
    result = sdk.fetch_order(id)
    assert result != None
    for field in expected_response.keys():
        assert result.__getattribute__(field) != None
        expected_value = expected_response[field]
        actual_value = result.__getattribute__(field)
        if field == "trades":
            for index in range(len(expected_value)):
                for trade_field in expected_value[index]:
                    expected_trade_value = expected_value[index][trade_field]
                    actual_trade_value = actual_value[index].__getattribute__(trade_field)
                    if trade_field == "amount" or trade_field == "price" or trade_field == "cost":
                        assert float(actual_trade_value) == float(expected_trade_value)
                    elif trade_field == "fee":
                        for fee_field in expected_trade_value:
                            if fee_field == "cost" or fee_field == "rate":
                                assert float(actual_trade_value[fee_field]) == float(
                                    expected_trade_value[fee_field]
                                )
                            else:
                                assert str(actual_trade_value[fee_field]) == str(
                                    expected_trade_value[fee_field]
                                )
                    elif (
                        trade_field == "datetime"
                        or trade_field == "timestamp"
                        or trade_field == "lastTradeTimestamp"
                        or trade_field == "info"
                    ):
                        continue
                    elif trade_field == "takerOrMaker":
                        assert actual_trade_value == expected_trade_value
                    else:
                        assert str(actual_trade_value) == str(expected_trade_value)
        elif field == "fee":
            for fee_field in expected_value:
                if fee_field == "cost" or fee_field == "rate":
                    assert float(actual_value[fee_field]) == float(expected_value[fee_field])
                else:
                    assert str(actual_value[fee_field]) == str(expected_value[fee_field])
        elif (
            field == "amount"
            or field == "price"
            or field == "average"
            or field == "filled"
            or field == "remaining"
            or field == "cost"
        ):
            assert float(actual_value) == float(expected_value)
        elif (
            field == "datetime"
            or field == "timestamp"
            or field == "lastTradeTimestamp"
            or field == "info"
        ):
            continue
        else:
            assert str(actual_value) == str(expected_value)


# def test_fetch_status() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
#     result = client.fetch_status()
#     assert "status" in result
#     assert result.get("status") == "success"
#     assert "updated" in result
#     assert "eta" in result
#     assert "url" in result


# def test_fetch_currencies() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.MAINNET)
#     result = client.fetch_currencies()
#     assert "BTC" in result
#     result_1: Any = result.get("BTC")
#     assert len(result_1) == 2


# def test_fetch_markets() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
#     result = client.fetch_markets()
#     assert "XRP/ETH" in result
#     result_1: Any = result.get("XRP/ETH")
#     assert "id" in result_1
#     assert "symbol" in result_1
#     assert "base" in result_1
#     assert "quote" in result_1
#     assert "quoteIssuer" in result_1
#     assert result_1.get("quote") == "ETH"


# def test_fetch_issuers() -> None:
#     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
#     result = client.fetch_issuers()
#     assert "Coreum" in result
#     result_1: Any = result.get("Coreum")
#     assert "name" in result_1
#     assert "trusted" in result_1
#     assert "website" in result_1
#     assert "currencies" in result_1
#     assert result_1.get("website") == "https://coreum.com"


# # def test_fetch_balance() -> None:
# #     client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
# #     result = client.fetch_balance("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib")
# #     assert "result" in result
# #     result_1: Any = result.get("result")
# #     assert "account" in result_1
# #     assert "status" in result_1
# #     assert result_1.get("account") == "r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"
# #     assert result_1.get("status") == "success"
# #     assert "ledger_current_index" in result_1


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
