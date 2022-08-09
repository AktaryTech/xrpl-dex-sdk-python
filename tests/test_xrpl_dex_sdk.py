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
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_TESTNET)
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
