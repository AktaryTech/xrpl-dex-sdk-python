import asyncio
from pprint import pprint
from xrpl_dex_sdk import models, constants, SDK, SDKParams
from xrpl.wallet import generate_faucet_wallet

#
#   Wallet A
#       - Load currencies, issuers, and markets
#       - Fetch market pairs and choose one
#       - Create trust line to issuer
#       - Fetch balances
#       - Check Order Book
#       - Place Buy Order
#       - Check Order status
#
#   Wallet B
#       - Load currencies, issuers, and markets
#       - Fetch market pairs and choose one
#       - Create trust line to issuer
#       - Fetch balances
#       - Check Order Book
#       - Place Sell Order
#       - Check Order status
#


async def use_sdk(sdk: SDK, name: str) -> None:
    print(f"{name} address: {sdk.wallet.classic_address}")

    # await sdk.load_currencies()
    # sdk.load_issuers()
    # await sdk.load_markets()

    # assert sdk.currencies
    # assert sdk.issuers
    # assert sdk.markets

    # # markets = await sdk.fetch_markets()
    # # if not markets:
    # #     return

    # # market = list(markets.keys())[1]

    # market = models.MarketSymbol.from_string(
    #     "XRP/TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd"
    # )

    # print("\nMarket")
    # print(market)

    # sdk.create_trust_line(code=market.quote, limit_amount="100000")

    # my_balances = await sdk.fetch_balance()

    # print("\nMy balances:")
    # print(my_balances)

    # order_book = sdk.fetch_order_book(symbol=market, limit=5)

    # print("\nOrder book")
    # print(order_book)

    # orders = await sdk.fetch_trades(
    #     symbol=models.MarketSymbol.from_string(
    #         "XRP/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"
    #     ),
    #     limit=5,
    # )
    order = await sdk.fetch_order(
        models.OrderId.from_string("rPWULQi9iEB3M3rGSoFoTLZDrkYmznhgrT:68056636")
    )
    print("\n order \n")
    print(order)

    # assert len(orders) == 5
    assert order

    # print("\n orders length \n")
    # print(len(orders))


#
# Address: rEQEwn35KoQdktQuXhRYiH9Q7hD6qZvHSi
# Secret: ssohaJJumUAxk1GZ1hj38aM8AzSBu
# Balance: 1,000 XRP
#


async def main() -> None:
    params = SDKParams(
        network=constants.MAINNET,
        wallet_secret="ssYqQi5KF8YaNQyMvZKP28uA7GbWq"
        # network=constants.TESTNET,
        # generate_wallet=True,
        # wallet_secret="ssohaJJumUAxk1GZ1hj38aM8AzSBu",
    )

    buyer_sdk = SDK(params)
    await use_sdk(buyer_sdk, "Buyer")

    # await use_sdk(
    #     SDK(
    #         SDKParams(
    #             # network=constants.MAINNET, wallet_secret="ssYqQi5KF8YaNQyMvZKP28uA7GbWq"
    #             network=constants.TESTNET,
    #             generate_wallet=True,
    #             fund_testnet_wallet=True,
    #         )
    #     ),
    #     "Seller",
    # )


def test() -> None:
    asyncio.run(main())


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


test()
