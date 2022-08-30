from typing import Any

import xrpl_dex_sdk


def test_version() -> None:
    assert xrpl_dex_sdk.__version__ == "0.1.0"


def test_fetch_status() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_TESTNET)
    result = client.fetch_status()
    assert "status" in result
    assert result.get("status") == "success"
    assert "updated" in result
    assert "eta" in result
    assert "url" in result


def test_fetch_currencies() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_MAINNET)
    result = client.fetch_currencies()
    assert "BTC" in result
    result_1: Any = result.get("BTC")
    assert len(result_1) == 2


def test_fetch_markets() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_TESTNET)
    result = client.fetch_markets()
    assert "XRP/ETH" in result
    result_1: Any = result.get("XRP/ETH")
    assert "id" in result_1
    assert "symbol" in result_1
    assert "base" in result_1
    assert "quote" in result_1
    assert "quoteIssuer" in result_1
    assert result_1.get("quote") == "ETH"


def test_fetch_issuers() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_TESTNET)
    result = client.fetch_issuers()
    assert "Coreum" in result
    result_1: Any = result.get("Coreum")
    assert "name" in result_1
    assert "trusted" in result_1
    assert "website" in result_1
    assert "currencies" in result_1
    assert result_1.get("website") == "https://coreum.com"


def test_fetch_balance() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_TESTNET)
    result = client.fetch_balance("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib")
    assert "result" in result
    result_1: Any = result.get("result")
    assert "account" in result_1
    assert "status" in result_1
    assert result_1.get("account") == "r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"
    assert result_1.get("status") == "success"
    assert "ledger_current_index" in result_1


def test_fetch_order_book() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_MAINNET)
    result = client.fetch_order_book(
        "XRP/USD",
        3,
        {
            "taker": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
            "taker_pays_issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
        },
    )
    assert "symbol" in result
    assert "nonce" in result
    assert "bids" in result
    assert "asks" in result


def test_fetch_order_books() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_MAINNET)
    result = client.fetch_order_books(
        ["XRP/USD"],
        3,
        {
            "XRP/USD": {
                "taker": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
                "taker_pays_issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
            },
        },
    )
    assert "XRP/USD" in result
    result_1: Any = result.get("XRP/USD")
    assert "symbol" in result_1
    assert "nonce" in result_1
    assert "bids" in result_1
    assert "asks" in result_1


def test_fetch_trading_fee() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_TESTNET)
    result = client.fetch_trading_fee("XRP/USD")
    assert "symbol" in result
    assert result.get("symbol") == "XRP/USD"
    assert "base" in result
    assert result.get("base") == 0
    assert "quote" in result
    assert result.get("quote") == 0
    assert "percentage" in result
    assert result.get("percentage") == True


def test_fetch_trading_fees() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_TESTNET)
    result = client.fetch_trading_fees()
    assert len(result) == 17
    result_1 = result[0]
    assert "symbol" in result_1
    assert result_1.get("symbol") == "534F4C4F00000000000000000000000000000000/XRP"
    assert "base" in result_1
    assert result_1.get("base") == 0
    assert "quote" in result_1
    assert result_1.get("quote") == 0
    assert "percentage" in result_1
    assert result_1.get("percentage") == True


def test_fetch_transaction_fee() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_MAINNET)
    result = client.fetch_transaction_fee("EUR")
    assert "code" in result
    assert "current" in result
    assert "info" in result
    assert "transfer" in result


def test_fetch_transaction_fees() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_MAINNET)
    result = client.fetch_transaction_fees(["EUR", "USD"])
    assert "code" in result[0]
    assert result[0].get("code") == "EUR"
    assert "current" in result[0]
    assert "info" in result[0]
    assert "transfer" in result[0]
    assert "code" in result[1]
    assert result[1].get("code") == "USD"
    assert "current" in result[1]
    assert "info" in result[1]
    assert "transfer" in result[1]


def test_fetch_fees() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_MAINNET)
    result = client.fetch_fees()
    assert "transactions" in result
    transactions: Any = result.get("transactions")
    assert "code" in transactions[0]
    assert "current" in transactions[0]
    assert "transfer" in transactions[0]
    assert "info" in transactions[0]
    trading: Any = result.get("trading")
    assert "symbol" in trading[0]
    assert "base" in trading[0]
    assert "quote" in trading[0]
    assert "percentage" in trading[0]
    assert "info" in trading[0]
