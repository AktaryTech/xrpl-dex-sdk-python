import xrpl_dex_sdk

client = xrpl_dex_sdk.Client(xrpl_dex_sdk.RPC_TESTNET)

# print(client.fetch_status())
print(client.fetch_currencies())
# print(client.fetch_markets())
# print(client.fetch_issuers())

# print(client.fetch_balance("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"))
# print(client.fetch_fees())
# print(client.fetch_trading_fee())
# print(client.fetch_trading_fees())
# print(client.fetch_transaction_fee())
# print(client.fetch_transaction_fees())
# print(client.fetch_order_book("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"))
# print(client.fetch_trades("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"))

# client.create_order()
# client.fetch_deposit()
# client.fetch_deposits()
