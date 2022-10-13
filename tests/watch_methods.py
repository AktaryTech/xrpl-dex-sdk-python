import asyncio
from pprint import pprint
from typing import Any
from xrpl_dex_sdk import SDK, constants


def balance_listener(data: Any):
    print("\ngot balance!\n")
    pprint(data)


def my_trades_listener(data: Any):
    print("\ngot my trades!\n")
    pprint(data)


def order_book_listener(data: Any):
    print("\ngot order_book!\n")
    pprint(data)


def orders_listener(data: Any):
    print("\ngot orders!\n")
    pprint(data)


def status_listener(data: Any):
    print("\ngot status!\n")
    pprint(data)


def ticker_listener(data: Any):
    print("\ngot ticker!\n")
    pprint(data)


def tickers_listener(data: Any):
    print("\ngot tickers!\n")
    pprint(data)


def trades_listener(data: Any):
    print("\ngot trades!\n")
    pprint(data)


async def main() -> None:
    sdk = SDK(
        {
            "network": constants.TESTNET,
            "wallet_secret": "shCwGCyy17Ph4JdZ6jTsFssEpS6Fs",
        }
    )

    asyncio.create_task(sdk.watch_balance(params={"listener": balance_listener}))
    asyncio.create_task(
        sdk.watch_my_trades(
            symbol="XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
            params={"listener": my_trades_listener},
        )
    )
    asyncio.create_task(
        sdk.watch_order_book(
            symbol="EUR+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP/CSC+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP",
            limit=None,
            params={"listener": order_book_listener},
        )
    )
    asyncio.create_task(sdk.watch_orders(symbol=None, params={"listener": orders_listener}))
    asyncio.create_task(sdk.watch_status(params={"listener": status_listener}))
    asyncio.create_task(
        sdk.watch_ticker(
            symbol="TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",
            params={"listener": ticker_listener},
        )
    )
    asyncio.create_task(
        sdk.watch_tickers(
            symbols=["TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP"],
            params={"listener": tickers_listener},
        )
    )
    asyncio.create_task(
        sdk.watch_trades(
            symbol="TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",
            params={"listener": trades_listener},
        )
    )

    await asyncio.sleep(25)


def test_watch_methods() -> None:
    asyncio.run(main())


test_watch_methods()
