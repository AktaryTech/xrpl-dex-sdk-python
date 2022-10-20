import pytest
from xrpl import asyncio, clients
from xrpl.utils import xrp_to_drops

from xrpl_dex_sdk import __version__, SDK, SDKParams, models, constants
from xrpl_dex_sdk.utils import hash_offer_id
from .fixtures import responses


test_json_rpc_url = constants.Networks[constants.TESTNET]["json_rpc"]
test_sync_client = clients.JsonRpcClient(test_json_rpc_url)
test_client = asyncio.clients.AsyncJsonRpcClient(test_json_rpc_url)

test_ws_url = constants.Networks[constants.TESTNET]["ws"]
test_websocket_client = asyncio.clients.AsyncWebsocketClient(test_ws_url)

test_wallet_secret = "shCwGCyy17Ph4JdZ6jTsFssEpS6Fs"
test_currency = "AKT"
test_issuer = "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
test_currency_code = test_currency + "+" + test_issuer

sdk_test_params = SDKParams(
    network=constants.TESTNET,
    sync_client=test_sync_client,
    client=test_client,
    wallet_secret=test_wallet_secret,
)


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_hash_offer_id() -> None:
    offer_id_hash_1 = hash_offer_id("rn5umFvUWKXqwrGJSRcV24wz9zZFiG7rsQ", 30419151)
    assert (
        offer_id_hash_1
        == "0D5A1CD41A637B533D123EE3408F898875E0F8FCA743CF98599E347F55D606DC"
    )
    offer_id_hash_2 = hash_offer_id("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z", 31617670)
    assert (
        offer_id_hash_2
        == "29B699A1C221904E43650999C5BA5C3B32E6416E4CA390E64EF4392FFACF4406"
    )


def test_ids() -> None:
    order_id = models.OrderId("rn5umFvUWKXqwrGJSRcV24wz9zZFiG7rsQ", 30419151)
    assert str(order_id) == "rn5umFvUWKXqwrGJSRcV24wz9zZFiG7rsQ:30419151"
    trade_id = models.TradeId.from_string("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z:31617670")
    assert trade_id.to_id() == "r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z:31617670"


def test_sdk() -> None:
    sdk = SDK(sdk_test_params)
    assert isinstance(sdk.client, asyncio.clients.AsyncJsonRpcClient)
    assert isinstance(sdk.sync_client, clients.JsonRpcClient)
    assert isinstance(sdk.websocket_client, asyncio.clients.AsyncWebsocketClient)
    assert sdk.wallet.classic_address == "rpkeJcxB2y5BeAFyycuWwdTTcR3og2a3SR"


def test_cancel_order() -> None:
    sdk = SDK(
        SDKParams(
            network=constants.TESTNET,
            client=test_client,
            generate_wallet=True,
            fund_testnet_wallet=True,
        )
    )
    create_result = sdk.create_limit_buy_order(
        symbol=models.MarketSymbol.from_string(f"{test_currency_code}/XRP"),
        amount=2,
        price=1.6,
    )
    assert create_result != None

    cancel_result = sdk.cancel_order(id=create_result.id)

    assert cancel_result != None
    assert str(cancel_result.id) == str(create_result.id)


def test_create_order() -> None:
    sdk = SDK(
        SDKParams(
            network=constants.TESTNET,
            client=test_client,
            generate_wallet=True,
            fund_testnet_wallet=True,
        )
    )

    amount = 2
    price = 2

    result = sdk.create_order(
        symbol=models.MarketSymbol.from_string(f"{test_currency_code}/XRP"),
        side=models.OrderSide.Buy,
        type=models.OrderType.Limit,
        amount=amount,
        price=price,
    )

    assert result != None

    tx = result.info["OfferCreate"]["tx_json"]
    assert tx != None
    assert tx["Account"] == sdk.wallet.classic_address
    assert tx["Flags"] & models.OfferCreateFlags.TF_SELL.value == 0
    assert tx["TakerGets"] == xrp_to_drops(amount * price)
    assert tx["TakerPays"]["currency"] == test_currency
    assert tx["TakerPays"]["issuer"] == test_issuer
    assert float(tx["TakerPays"]["value"]) == amount


def test_create_limit_buy_order() -> None:
    sdk = SDK(
        SDKParams(
            network=constants.TESTNET,
            client=test_client,
            generate_wallet=True,
            fund_testnet_wallet=True,
        )
    )

    amount = 2
    price = 2

    result = sdk.create_limit_buy_order(
        symbol=models.MarketSymbol.from_string(f"{test_currency_code}/XRP"),
        amount=amount,
        price=price,
    )
    assert result != None

    tx = result.info["OfferCreate"]["tx_json"]
    assert tx != None
    assert tx["Account"] == sdk.wallet.classic_address
    assert tx["Flags"] & models.OfferCreateFlags.TF_SELL.value == 0
    assert tx["TakerGets"] == xrp_to_drops(amount * price)
    assert tx["TakerPays"]["currency"] == test_currency
    assert tx["TakerPays"]["issuer"] == test_issuer
    assert float(tx["TakerPays"]["value"]) == amount


def test_create_limit_sell_order() -> None:
    sdk = SDK(
        SDKParams(
            network=constants.TESTNET,
            client=test_client,
            generate_wallet=True,
            fund_testnet_wallet=True,
        )
    )

    amount = 5
    price = 1.5

    result = sdk.create_limit_sell_order(
        symbol=models.MarketSymbol.from_string(f"{test_currency_code}/XRP"),
        amount=amount,
        price=price,
    )
    assert result != None

    tx = result.info["OfferCreate"]["tx_json"]
    assert tx != None
    assert tx["Account"] == sdk.wallet.classic_address
    assert (
        tx["Flags"] & models.OfferCreateFlags.TF_SELL.value
        == models.OfferCreateFlags.TF_SELL.value
    )
    assert tx["TakerPays"] == xrp_to_drops(amount * price)
    assert tx["TakerGets"]["currency"] == test_currency
    assert tx["TakerGets"]["issuer"] == test_issuer
    assert float(tx["TakerGets"]["value"]) == amount


def test_create_trust_line() -> None:
    sdk = SDK(
        SDKParams(
            network=constants.TESTNET,
            client=test_client,
            generate_wallet=True,
            fund_testnet_wallet=True,
        )
    )
    create_result = sdk.create_trust_line(
        code=models.CurrencyCode(test_currency, test_issuer), limit_amount="1000000"
    )
    assert create_result != None


@pytest.mark.asyncio
async def test_fetch_balance() -> None:
    sdk = SDK(sdk_test_params)
    balances = await sdk.fetch_balance()
    assert balances != None
    assert balances.balances != None
    assert balances.info != None
    assert models.CurrencyCode("XRP") in balances.balances
    assert balances.info["account_info"]["Account"] == sdk.wallet.classic_address


@pytest.mark.asyncio
async def test_fetch_canceled_orders() -> None:
    sdk = SDK(sdk_test_params)
    symbol = models.MarketSymbol(
        models.CurrencyCode.from_string("XRP"),
        models.CurrencyCode.from_string("USD+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
    )

    result = await sdk.fetch_canceled_orders(
        symbol, None, 1, models.FetchCanceledOrdersParams(search_limit=25)
    )

    assert result != None


@pytest.mark.asyncio
async def test_fetch_closed_orders() -> None:
    sdk = SDK(sdk_test_params)
    symbol = models.MarketSymbol(
        models.CurrencyCode.from_string("XRP"),
        models.CurrencyCode.from_string("USD+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
    )

    result = await sdk.fetch_closed_orders(
        symbol, None, 1, models.FetchClosedOrdersParams(search_limit=25)
    )

    assert result != None


@pytest.mark.asyncio
async def test_fetch_currencies() -> None:
    sdk = SDK(SDKParams(network=constants.MAINNET, wallet_secret=test_wallet_secret))
    currencies = await sdk.fetch_currencies()
    assert currencies != None
    assert currencies == responses.fetch_currencies_response


@pytest.mark.asyncio
async def test_fetch_fees() -> None:
    sdk = SDK(sdk_test_params)
    result = await sdk.fetch_fees()
    print(result)
    transactions = result.transactions
    assert transactions != None
    assert transactions[0].code != None
    assert transactions[0].current != None
    assert transactions[0].transfer != None
    assert transactions[0].info != None
    trading = result.trading
    assert trading != None
    assert trading[0].symbol != None
    assert trading[0].base != None
    assert trading[0].quote != None
    assert trading[0].percentage != None
    assert trading[0].info != None


def test_fetch_issuers() -> None:
    sdk = SDK(SDKParams(network=constants.MAINNET, wallet_secret=test_wallet_secret))
    issuers = sdk.fetch_issuers()
    print("issuers")
    print(issuers)
    assert issuers != None
    # assert issuers == responses.fetch_issuers_response


@pytest.mark.asyncio
async def test_fetch_l2_order_book() -> None:
    sdk = SDK(sdk_test_params)
    test_limit = 3
    test_symbol = models.MarketSymbol.from_string(
        "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP"
    )
    order_book: models.OrderBook = await sdk.fetch_l2_order_book(
        symbol=test_symbol,
        limit=test_limit,
        params=models.FetchL2OrderBookParams(taker=sdk.wallet.classic_address),
    )

    expected_order_book = responses.fetch_order_book_response[test_symbol]
    assert order_book.symbol == expected_order_book.symbol
    assert order_book.nonce == expected_order_book.nonce
    assert order_book.bids == expected_order_book.bids
    assert order_book.asks == expected_order_book.asks
    assert len(order_book.bids) + len(order_book.asks) == test_limit


@pytest.mark.asyncio
async def test_fetch_market() -> None:
    sdk = SDK(SDKParams(network=constants.MAINNET, wallet_secret=test_wallet_secret))
    market = await sdk.fetch_market(
        "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/XRP"
    )
    print("market")
    print(market)
    assert market != None
    # assert markets == responses.fetch_markets_response


@pytest.mark.asyncio
async def test_fetch_markets() -> None:
    sdk = SDK(SDKParams(network=constants.MAINNET, wallet_secret=test_wallet_secret))
    markets = await sdk.fetch_markets()
    print("markets")
    print(markets)
    assert markets != None
    # assert markets == responses.fetch_markets_response


@pytest.mark.asyncio
async def test_fetch_my_trades() -> None:
    sdk = SDK(sdk_test_params)
    # TODO: mock up this response
    my_trades = await sdk.fetch_my_trades(
        symbol=models.MarketSymbol.from_string(
            "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
        ),
        limit=3,
    )
    assert my_trades != None
    assert len(my_trades) == 3


@pytest.mark.asyncio
async def test_fetch_open_orders() -> None:
    sdk = SDK(sdk_test_params)
    symbol = models.MarketSymbol(
        models.CurrencyCode.from_string("XRP"),
        models.CurrencyCode.from_string("USD+rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP"),
    )

    result = await sdk.fetch_open_orders(
        symbol, None, 1, models.FetchOpenOrdersParams(search_limit=25)
    )

    assert result != None


@pytest.mark.asyncio
async def test_fetch_order_book() -> None:
    sdk = SDK(sdk_test_params)
    test_limit = 3
    test_symbol = models.MarketSymbol.from_string(
        "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP"
    )
    order_book: models.OrderBook = await sdk.fetch_order_book(
        symbol=test_symbol,
        limit=test_limit,
        params=models.FetchOrderBookParams(taker=sdk.wallet.classic_address),
    )

    expected_order_book = responses.fetch_order_book_response[test_symbol]
    assert order_book.symbol == expected_order_book.symbol
    assert order_book.nonce == expected_order_book.nonce
    assert order_book.bids == expected_order_book.bids
    assert order_book.asks == expected_order_book.asks
    assert len(order_book.bids) + len(order_book.asks) == test_limit


@pytest.mark.asyncio
async def test_fetch_order_books() -> None:
    sdk = SDK(sdk_test_params)
    test_limit = 3
    test_symbol = models.MarketSymbol.from_string(
        "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP"
    )
    order_books: models.OrderBooks = await sdk.fetch_order_books(
        symbols=[test_symbol],
        limit=test_limit,
        params=models.FetchOrderBooksParams(
            symbols={
                test_symbol: models.FetchOrderBookParams(
                    taker=sdk.wallet.classic_address
                )
            },
        ),
    )

    assert test_symbol in order_books
    order_book_1 = order_books[test_symbol]

    expected_order_book = responses.fetch_order_book_response[test_symbol]
    assert order_book_1.symbol == expected_order_book.symbol
    assert order_book_1.nonce == expected_order_book.nonce
    assert order_book_1.bids == expected_order_book.bids
    assert order_book_1.asks == expected_order_book.asks
    assert len(order_book_1.bids) + len(order_book_1.asks) == test_limit


@pytest.mark.asyncio
async def test_fetch_order() -> None:
    sdk = SDK(sdk_test_params)
    id = models.OrderId("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z", 31617670)
    expected_response = responses.fetch_order_responses[id]

    order = await sdk.fetch_order(id)

    assert order != None
    assert order.id == expected_response.id
    assert order.client_order_id == expected_response.client_order_id
    assert str(order.timestamp) in str(expected_response.timestamp)
    assert str(order.last_trade_timestamp) in str(
        expected_response.last_trade_timestamp
    )
    assert order.status == expected_response.status
    assert str(order.symbol) == str(expected_response.symbol)
    assert order.type == expected_response.type
    assert order.time_in_force == expected_response.time_in_force
    assert order.side == expected_response.side
    assert order.amount == expected_response.amount
    assert order.price == expected_response.price
    assert len(order.trades)


@pytest.mark.asyncio
async def test_fetch_orders() -> None:
    sdk = SDK(sdk_test_params)
    symbol = models.MarketSymbol.from_string(
        "XRP/USD+r3ah58KQsfqaQ3uwngknBzA2h2bRSZTrjx"
    )

    orders = await sdk.fetch_orders(symbol, None, 1)

    assert orders != None


@pytest.mark.asyncio
async def test_fetch_status() -> None:
    sdk = SDK(sdk_test_params)
    status = await sdk.fetch_status()
    assert status != None


@pytest.mark.asyncio
async def test_fetch_ticker() -> None:
    sdk = SDK(sdk_test_params)
    ticker = await sdk.fetch_ticker(
        models.MarketSymbol.from_string("TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP")
    )
    assert ticker != None


@pytest.mark.asyncio
async def test_fetch_tickers() -> None:
    sdk = SDK(sdk_test_params)
    tickers = await sdk.fetch_tickers(
        [
            models.MarketSymbol.from_string(
                "TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP"
            ),
            models.MarketSymbol.from_string(
                "XRP/TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd"
            ),
        ]
    )
    assert tickers != None
    assert len(tickers) == 2


@pytest.mark.asyncio
async def test_fetch_trades() -> None:
    sdk = SDK(sdk_test_params)
    trades = await sdk.fetch_trades(
        symbol=models.MarketSymbol.from_string(
            "XRP/USD+r3ah58KQsfqaQ3uwngknBzA2h2bRSZTrjx"
        ),
        limit=1,
        params=models.FetchTradesParams(search_limit=100),
    )
    assert trades != None
    # TODO: mock up these responses (too hard to find a real testnet pair with recent trades)
    # assert len(trades) > 0


@pytest.mark.asyncio
async def test_fetch_trading_fee() -> None:
    sdk = SDK(sdk_test_params)
    test_symbol = models.MarketSymbol.from_string(
        "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
    )
    trading_fee = await sdk.fetch_trading_fee(test_symbol)
    assert trading_fee != None
    assert trading_fee.symbol != None
    assert str(trading_fee.symbol) == str(test_symbol)
    assert trading_fee.base == 0
    assert trading_fee.quote == 0.005
    assert trading_fee.percentage == True


@pytest.mark.asyncio
async def test_fetch_trading_fees() -> None:
    sdk = SDK(sdk_test_params)
    trading_fees = await sdk.fetch_trading_fees()

    assert len(trading_fees) == 2

    def sort_fees(fee: models.TradingFee):
        return str(fee.symbol)

    trading_fees.sort(reverse=False, key=sort_fees)

    trading_fee_1 = trading_fees[0]
    trading_fee_2 = trading_fees[1]

    assert trading_fee_1.symbol != None
    assert str(trading_fee_1.symbol) == "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP"
    assert trading_fee_1.base == 0.005
    assert trading_fee_1.quote == 0
    assert trading_fee_1.percentage == True

    assert trading_fee_2.symbol != None
    assert str(trading_fee_2.symbol) == "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
    assert trading_fee_2.base == 0
    assert trading_fee_2.quote == 0.005
    assert trading_fee_2.percentage == True


@pytest.mark.asyncio
async def test_fetch_transaction_fee() -> None:
    sdk = SDK(sdk_test_params)
    transaction_fee = await sdk.fetch_transaction_fee(
        models.CurrencyCode.from_string("AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B")
    )
    assert transaction_fee != None
    assert transaction_fee.code != None
    assert transaction_fee.current != None
    assert transaction_fee.transfer != None
    assert transaction_fee.info != None


@pytest.mark.asyncio
async def test_fetch_transaction_fees() -> None:
    sdk = SDK(sdk_test_params)
    transaction_fees = await sdk.fetch_transaction_fees(
        [models.CurrencyCode.from_string("AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B")]
    )
    assert transaction_fees != None and len(transaction_fees) > 0
    assert transaction_fees[0].code != None
    assert str(transaction_fees[0].code) == "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
    assert transaction_fees[0].current != None
    assert transaction_fees[0].transfer != None
    assert transaction_fees[0].info != None


@pytest.mark.asyncio
async def test_fetch_transfer_rate() -> None:
    sdk = SDK(sdk_test_params)
    transfer_rate = await sdk.fetch_transfer_rate(
        issuer="rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"  # our test issuer
    )
    assert transfer_rate != None
    assert transfer_rate == 0.005


@pytest.mark.asyncio
async def test_load_currencies() -> None:
    sdk = SDK(sdk_test_params)
    await sdk.load_currencies()
    assert sdk.currencies != None


def test_load_issuers() -> None:
    sdk = SDK(sdk_test_params)
    sdk.load_issuers()
    assert sdk.issuers != None


@pytest.mark.asyncio
async def test_load_markets() -> None:
    sdk = SDK(sdk_test_params)
    await sdk.load_markets()
    assert sdk.markets != None
