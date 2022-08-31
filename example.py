import asyncio

import xrpl_dex_sdk

# client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_TESTNET)
# client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_MAINNET)

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


def foo(data):
    print("foo=> ", data)


async def main() -> None:
    client = xrpl_dex_sdk.Client(xrpl_dex_sdk.WS_TESTNET)
    # await client.watch_status(foo)
    # await client.watch_order_book("USD/XRP", "rJ9D95MwHFHxDDyeBg4SG644wPYqyEGsE7", foo)
    # await client.watch_transactions(["rJ9D95MwHFHxDDyeBg4SG644wPYqyEGsE7"], foo)
    # await client.watch_my_trades("rhvXHRpiWhuXAztZiz3f4AgVr3jwPmNmVv", foo)
    # await client.watch_balance("rhvXHRpiWhuXAztZiz3f4AgVr3jwPmNmVv", foo)
    await client.watch_create_order("rhvXHRpiWhuXAztZiz3f4AgVr3jwPmNmVv", foo)


asyncio.run(main())

# RAW
# print(client.fetch_trades("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"))
