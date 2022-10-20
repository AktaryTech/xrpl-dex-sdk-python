import asyncio
import json
from typing import Any
from uuid import uuid4

import xrpl_dex_sdk

# client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
# client = xrpl_dex_sdk.Client(xrpl_dex_sdk.MAINNET)

# print(client.fetch_status())
# print(client.fetch_currencies())
# print(client.fetch_markets())
# print(client.fetch_issuers())
# print(client.fetch_balance("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"))
# print(
#     client.fetch_order_book(
#         "XRP/USD",
#         3,
#         {
#             "taker": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
#             "taker_pays_issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#         },
#     )
# )

# print(
#     client.fetch_order_books(
#         ["XRP/USD"],
#         3,
#         {
#             "XRP/USD": {
#                 "taker": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
#                 "taker_pays_issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#             },
#         },
#     )
# )
# print(client.fetch_trading_fee("XRP/USD"))
# print(client.fetch_trading_fees())
# print(client.fetch_transaction_fee("EUR"))
# print(client.fetch_transaction_fees(["EUR", "USD"]))
# print(client.fetch_fees())


def foo(data: Any) -> None:
    print(json.dumps(data, indent=4))


def write_to_out(data: Any) -> None:

    f = open("./out/" + uuid4().hex, "w")
    f.write(json.dumps(data, indent=4))
    f.close()


async def main() -> None:
    # client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
    sdk = xrpl_dex_sdk.SDK(
        {
            "network": xrpl_dex_sdk.constants.TESTNET,
            "wallet_secret": "shCwGCyy17Ph4JdZ6jTsFssEpS6Fs",
        }
    )

    await sdk.watch_balance(foo)
    # await client.watch_status(foo)
    # await client.watch_order_book(foo, "XRP/EUR")
    # await client.watch_transactions(foo, ["rJ9D95MwHFHxDDyeBg4SG644wPYqyEGsE7"])
    # await client.watch_my_trades(foo, "rhLSGdavS2B3NVDQX23rQ9zaRrBcKb96BP")
    # await client.watch_balance(foo, "rhLSGdavS2B3NVDQX23rQ9zaRrBcKb96BP")
    # await client.watch_create_order(foo, "rhvXHRpiWhuXAztZiz3f4AgVr3jwPmNmVv")
    # await client.watch_cancel_order(foo, "rhvXHRpiWhuXAztZiz3f4AgVr3jwPmNmVv")
    # await client.watch_orders(write_to_out, "EUR/USD")
    # await client.watch_trades(write_to_out, "EUR/USD")
    # await client.watch_ticker(foo, "XRP/EUR")
    # await client.watch_tickers(foo, ["XRP/EUR", "XRP/USD", "XRP/ETH", "BTC/USD"])
    # await client.watch_ledger(foo)


asyncio.run(main())

# RAW
# print(client.fetch_trades("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"))
