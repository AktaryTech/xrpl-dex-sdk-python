import json

import xrpl_dex_sdk_python


def test_version() -> None:
    assert xrpl_dex_sdk_python.__version__ == "0.1.0"


def test_fetch_balance() -> None:
    client = xrpl_dex_sdk_python.Client(xrpl_dex_sdk_python.testnet)
    result = json.loads(client.fetch_balance("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib").text)
    assert "result" in result
    result_1 = result.get("result")
    assert "account" in result_1
    assert "status" in result_1
    assert result_1.get("account") == "r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"
    assert result_1.get("status") == "success"
    assert "ledger_current_index" in result_1
