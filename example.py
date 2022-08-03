import xrpl_dex_sdk

client = xrpl_dex_sdk.Client(xrpl_dex_sdk.testnet)

print(client.fetch_balance("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib").text)
print(client.fetch_status().text)
print(client.fetch_fees().text)
print(client.fetch_trading_fee().text)
print(client.fetch_trading_fees().text)
print(client.fetch_transaction_fee().text)
print(client.fetch_transaction_fees().text)
print(client.fetch_order_book("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib").text)
print(client.fetch_trades("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib").text)

# client.fetch_markets()
# client.fetch_currencies()
# client.create_order()
# client.fetch_deposit()
# client.fetch_deposits()
