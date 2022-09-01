import datetime
import json
import os
import uuid
from enum import Enum
from typing import Any, Callable, Dict, List, Tuple, Union

import requests
from websockets.client import connect as ws_connect
from xrpl import utils, wallet
from xrpl.asyncio import transaction
from xrpl.models import transactions

# import websockets

__version__ = "0.1.0"

# const
LIMIT: int = int(os.getenv("RIPPLE_DEFAULT_LIMIT", 20))

TESTNET: str = "TESTNET"
DEVNET: str = "DEVNET"
MAINNET: str = "MAINNET"

TESTNET_URL: str = os.getenv("RIPPLE_TESTNET_URL", "s.altnet.rippletest.net")
DEVNET_URL: str = os.getenv("RIPPLE_DEVNET_URL", "s.devnet.rippletest.net")
MAINNET_URL: str = os.getenv("RIPPLE_MAINNET_URL", "s1.ripple.com")

RPC_TESTNET: str = "https://" + TESTNET_URL + ":51234/"
RPC_DEVNET: str = "https://" + DEVNET_URL + ":51234/"
RPC_MAINNET: str = "https://" + MAINNET_URL + ":51234/"

WS_TESTNET: str = "wss://" + TESTNET_URL + ":51233/"
WS_DEVNET: str = "wss://" + DEVNET_URL + ":51233/"
WS_MAINNET: str = "wss://" + MAINNET_URL + "/"


REFERENCE_TX_COST: int = 10
ACCOUNT_DELETE_TX_COST: int = 2000000

BILLION: int = 1000000000


class OrderStatus(Enum):
    Open: str = "open"
    Closed: str = "closed"
    Canceled: str = "canceled"
    Expired: str = "expired"
    Rejected: str = "rejected"


class OrderType(Enum):
    Limit: str = "limit"
    Market: str = "market"


class OrderTimeInForce(Enum):
    GoodTillCanceled: str = "gtc"
    ImmediateOrCancel: str = "ioc"
    FillOrKill: str = "fok"
    PostOnly: str = "po"


class OrderSide(Enum):
    Buy: str = "buy"
    Sell: str = "sell"


class Client:
    """A json-rpc client class"""

    def __init__(self, network: str = MAINNET) -> None:
        """Return client instant, pass in network, defaults to mainnet"""
        self._cache: Any = {}
        if network == MAINNET:
            self.ws_url = WS_MAINNET
            self.rpc_url = RPC_MAINNET
        elif network == TESTNET:
            self.ws_url = WS_TESTNET
            self.rpc_url = RPC_TESTNET
        elif network == DEVNET:
            self.ws_url = WS_DEVNET
            self.rpc_url = RPC_DEVNET

    async def subscribe(
        self, payload: str, listener: Callable, transform: Callable, extra: Tuple
    ) -> None:
        """subscribes to stream"""
        connection = ws_connect(uri=self.ws_url)
        async with connection as websocket:
            print(json.dumps(json.loads(payload), indent=4))
            await websocket.send(payload)
            initialized = False
            async for message in websocket:
                json_message = json.loads(message)
                if initialized is False:
                    print(json.dumps(json_message, indent=4))
                    if json_message.get("status") == "success":
                        initialized = True
                        continue
                    else:
                        raise Exception(message)

                # call function passed in with data
                transformed = transform(json_message, extra)
                # return none from transformed to prevent message callback
                if transformed:
                    listener(transformed)

    def json_rpc(self, payload: Any) -> Any:
        """calls the json_rpc api with requests returning json dict"""
        return json.loads(requests.post(self.rpc_url, json=payload).text)

    def load_data(self, name: str) -> Dict:
        path = os.path.dirname(os.path.realpath(__file__)) + os.sep + "data" + os.sep + name
        f = open(path, "r")
        data = f.read()
        f.close()
        return json.loads(data)

    def transfer_rate_to_decimal(self, rate: int) -> str:
        if rate != int(rate):
            raise Exception("Error decoding, transfer Rate must be an integer")

        if rate == 0:
            return "0"

        decimal = (rate - BILLION) / BILLION

        if decimal < 0:
            raise Exception("Error decoding, negative transfer rate")

        return str(decimal)

    def offer_create_flags_to_time_in_force(self, tx: Any) -> str:
        # setTransactionFlagsToNumber(tx)
        flags = float(tx.get("Flags"))
        if flags == 0 and not tx.get("Expiration"):
            return OrderTimeInForce.GoodTillCanceled.value
        elif (
            flags
            and transactions.OfferCreateFlags.tfFillOrKill
            == transactions.OfferCreateFlags.tfFillOrKill
        ):
            return OrderTimeInForce.FillOrKill.value
        elif (
            flags
            and transactions.OfferCreateFlags.tfImmediateOrCancel
            == transactions.OfferCreateFlags.tfImmediateOrCancel
        ):
            return OrderTimeInForce.ImmediateOrCancel.value
        elif (
            flags
            and transactions.OfferCreateFlags.tfPassive == transactions.OfferCreateFlags.tfPassive
        ):
            return OrderTimeInForce.PostOnly.value
        else:
            return OrderTimeInForce.PostOnly.value

    def transform_status(self, data: Dict) -> Dict:
        status = data.get("status")
        state: Any = data.get("state")
        if state.get("server_state") == "disconnected":
            status = "shutdown"
        updated = int(
            datetime.datetime.strptime(state.get("time"), "%Y-%b-%d %H:%M:%S.%f %Z").timestamp()
            * 1000
        )
        return {"status": status, "updated": updated, "eta": "", "url": ""}

    def fetch_status(self) -> Dict:
        # server_state
        payload = {"method": "server_state", "params": [{}]}
        result = self.json_rpc(payload).get("result")
        return self.transform_status(result)

    async def watch_status(self, listener: Callable) -> Dict:
        id = uuid.uuid4().hex
        payload = '{ "id": "' + id + '", "command":"subscribe", "streams":["server"] }'
        extra = ()
        await self.subscribe(payload, listener, self.transform_status, extra)
        return {}

    def fetch_currencies(self) -> Dict:
        if "fetch_currencies" in self._cache:
            return self._cache.get("fetch_currencies")
        currencies = self.load_data("currencies.json")
        for _, currency in currencies.items():
            for curr in currency:
                payload = {"method": "account_info", "params": [{"account": curr.get("issuer")}]}
                account_info_result = self.json_rpc(payload).get("result")
                account_rate = account_info_result.get("account_data").get("TransferRate")
                if account_rate:
                    curr["fee"] = self.transfer_rate_to_decimal(account_rate)
        self._cache["fetch_currencies"] = currencies
        return currencies

    def fetch_markets(self) -> Dict:
        return self.load_data("markets.json")

    def fetch_issuers(self) -> Dict:
        return self.load_data("issuers.json")

    def fetch_balance(self, account: str) -> Dict:
        # gateway_balances
        payload = {"method": "gateway_balances", "params": [{"account": account}]}
        return self.json_rpc(payload)

    def fetch_fees(self) -> Dict:
        currencies: Any = self.fetch_currencies()
        transactions = self.fetch_transaction_fees(currencies.keys())
        trading = self.fetch_trading_fees()

        return {"transactions": transactions, "trading": trading}

    def fetch_trading_fee(self, symbol: str) -> Dict:
        markets = self.fetch_markets()
        if symbol in markets is False:
            raise Exception("No symbol in markets data")

        market_symbol: Any = markets.get(symbol)
        base_fee = market_symbol.get("baseFee", 0)
        base_issuer = market_symbol.get("baseIssuer")
        quote_fee = market_symbol.get("quoteFee", 0)
        quote_issuer = market_symbol.get("quoteIssuer")
        response: Any = {
            "symbol": symbol,
            "base": base_fee,
            "quote": quote_fee,
            "percentage": True,
            "info": json.dumps({"market": market_symbol}),
        }
        if base_issuer:
            response["baseIssuer"] = base_issuer
        if quote_issuer:
            response["quoteIssuer"] = quote_issuer

        return response

    def fetch_trading_fees(self) -> list:
        markets = self.fetch_markets()
        result: list = []
        for market in markets:
            result.append(self.fetch_trading_fee(market))
        return result

    def fetch_transaction_fee(self, code: str, params: Dict = {}) -> Dict:
        payload = {"method": "fee", "params": [{}]}
        fees_result = self.json_rpc(payload).get("result")

        currencies = self.fetch_currencies()
        if code in currencies is False:
            raise Exception("No code in currencies data")

        transfer_rates: Any = {}

        currency: Any = currencies.get(code)

        params_issuer = params.get("issuer")
        for curr in currency:
            fee = curr.get("fee", 0)
            issuer = curr.get("issuer")
            if "issuer" in params:
                if params_issuer == issuer:
                    transfer_rates[issuer] = fee
            else:
                transfer_rates[issuer] = fee

        response: Any = {
            "code": code,
            "current": int(fees_result.get("drops").get("open_ledger_fee")),
            "transfer": transfer_rates,
            "info": json.dumps({"feesResult": fees_result, "currency": currency}),
        }

        return response

    def fetch_transaction_fees(self, codes: list, params: dict = {}) -> list:
        response: list = []
        for code in codes:
            param = params.get("code", {})
            response.append(self.fetch_transaction_fee(code, param))
        return response

    async def create_order(
        self, symbol: str, side: str, type: str, amount: str, price: str, params: dict
    ) -> Dict:
        [base, quote] = symbol.split("/")
        wallet_private_key = params.get("wallet_private_key")
        wallet_public_key = params.get("wallet_public_key")
        wallet_secret = params.get("wallet_secret")
        wallet_sequence = params.get("wallet_sequence")
        taker_gets_issuer = params.get("taker_gets_issuer", "")
        taker_pays_issuer = params.get("taker_pays_issuer", "")
        expiration = params.get("expiration", None)
        memos = params.get("memos", None)
        flags = params.get("flags", None)

        creator_gets_currency = quote if side == "buy" else base
        creator_gets_amount = amount
        creator_pays_currency = quote if side == "buy" else base
        creator_pays_amount = price

        if creator_gets_currency == "XRP":
            creator_gets: Any = creator_gets_amount
        else:
            creator_gets = {
                "currency": creator_gets_currency,
                "value": creator_gets_amount,
                "issuer": taker_pays_issuer,
            }
        if creator_pays_currency == "XRP":
            creator_pays: Any = creator_pays_amount
        else:
            creator_pays = {
                "currency": creator_pays_currency,
                "value": creator_pays_amount,
                "issuer": taker_gets_issuer,
            }

        if not wallet_secret and (not wallet_public_key or not wallet_private_key):
            raise Exception(
                "Must provide either wallet_secret or wallet_public_key and wallet_private_key"
            )

        the_wallet = wallet.Wallet(seed=wallet_secret, sequence=wallet_sequence)

        offer_create = transactions.OfferCreate(
            account=the_wallet.classic_address,
            sequence=the_wallet.sequence,
            taker_gets=creator_pays,
            taker_pays=creator_gets,
            expiration=expiration,
            memos=memos,
            flags=flags,
        )

        offer_create_response: Any = await transaction.safe_sign_and_submit_transaction(
            offer_create,
            the_wallet,
        )

        amountFilled = 0
        amountRemaining = float(creator_gets_amount)

        status = OrderStatus.Open.value

        # TODO: fill this in once the Trades logic is complete
        trades: List[Any] = []

        # TODO: calculate lastTradeTimestamp once Trades logic is complete
        last_trade_timestamp = 0

        # TODO: properly calculate this once Trades logic is complete
        average = 0

        newOrder = {
            "id": str(offer_create_response.get("result").get("Sequence", 0)),
            "datetime": utils.ripple_time_to_datetime(
                offer_create_response.get("result").get("date", 0)
            ),
            "timestamp": utils.ripple_time_to_posix(
                offer_create_response.get("result").get("date", 0)
            ),
            "last_trade_timestamp": last_trade_timestamp,
            "status": status,
            "symbol": symbol,
            "type": type,
            "time_in_force": self.offer_create_flags_to_time_in_force(offer_create),
            "side": side,
            "price": float(price),
            "average": average,
            "amount": float(amount),
            "filled": amountFilled,
            "remaining": amountRemaining,
            "cost": amountFilled * float(price),
            "trades": trades,
            "fee": {
                "currency": "XRP",
                "cost": float(offer_create_response.get("result").get("Fee", REFERENCE_TX_COST)),
            },
            "info": {"OfferCreate": offer_create_response.get("result")},
        }

        return newOrder

    async def create_limit_buy_order(
        self, symbol: str, amount: str, price: str, params: dict
    ) -> Dict:
        return await self.create_order(
            symbol, OrderSide.Buy.value, OrderType.Limit.value, amount, price, params
        )

    async def create_limit_sell_order(
        self, symbol: str, side: str, type: str, amount: str, price: str, params: dict
    ) -> Dict:
        return await self.create_order(
            symbol, OrderSide.Sell.value, OrderType.Limit.value, amount, price, params
        )

    async def cancel_order(self, id: str, params: Dict) -> Dict:
        # offer_cancel
        wallet_private_key = params.get("wallet_private_key")
        wallet_public_key = params.get("wallet_public_key")
        wallet_secret = params.get("wallet_secret")

        wallet_sequence = int(id)
        if not wallet_sequence:
            raise Exception("Must provide sequence id")

        if not wallet_secret and (not wallet_public_key or not wallet_private_key):
            raise Exception(
                "Must provide either wallet_secret or wallet_public_key and wallet_private_key"
            )
        the_wallet = wallet.Wallet(seed=wallet_secret, sequence=wallet_sequence)

        offer_cancel = transactions.OfferCancel(
            account=the_wallet.classicAddress,
            transaction_type="OfferCancel",
            offer_sequence=wallet_sequence,
        )

        offer_cancel_result = await transaction.safe_sign_and_submit_transaction(
            offer_cancel, {"autofill": True, "wallet": the_wallet}
        )

        response = {
            "id": id,
            "info": {"OfferCancel": offer_cancel_result},
        }

        return response

    def fetch_order_books(self, symbols: list, limit: int = LIMIT, params: Any = {}) -> Dict:
        order_books: Any = {}
        for symbol in symbols:
            order_books.setdefault(symbol, self.fetch_order_book(symbol, limit, params.get(symbol)))
        return order_books

    def transform_order_book(self, data: Any, extra: Any) -> Dict:
        return data

    async def watch_order_book(self, listener: Callable, symbol: str, taker: str = "") -> Dict:
        markets: Any = self.fetch_markets()
        if symbol not in markets:
            raise Exception("symbol not in markets")
        market: Any = markets.get(symbol)
        id = uuid.uuid4().hex
        [base, quote] = symbol.split("/")
        taker_pays = {
            "currency": quote,
        }
        if "quoteIssuer" in market:
            taker_pays["issuer"] = market.get("quoteIssuer")

        taker_gets = {"currency": base}
        if "baseIssuer" in market:
            taker_gets["issuer"] = market.get("baseIssuer")
        payload: Any = {
            "id": id,
            "command": "subscribe",
            "books": [{"taker_pays": taker_pays, "taker_gets": taker_gets}],
        }
        if taker:
            payload.get("books")[0]["taker"] = taker
        extra = ()
        await self.subscribe(json.dumps(payload), listener, self.transform_order_book, extra)
        return {}

    def fetch_order_book(self, symbol: str, limit: int = LIMIT, params: Any = {}) -> Dict:
        [base, quote] = symbol.split("/")
        taker_pays = {
            "currency": quote,
        }
        if "taker_pays_issuer" in params:
            taker_pays["issuer"] = params.get("taker_pays_issuer")

        taker_gets = {
            "currency": base,
        }
        if "taker_gets_issuer" in params:
            taker_gets["issuer"] = params.get("taker_gets_issuer")

        # book_offers
        payload: Any = {
            "method": "book_offers",
            "params": [
                {
                    "taker_gets": taker_gets,
                    "taker_pays": taker_pays,
                    "limit": limit,
                }
            ],
        }

        if "ledger_index" in params:
            payload.get("params")[0]["ledger_index"] = params.get("ledger_index")

        if "ledger_hash" in params:
            payload.get("params")[0]["ledger_hash"] = params.get("ledger_hash")

        if "taker" in params:
            payload.get("params")[0]["taker"] = params.get("taker")

        result = self.json_rpc(payload)

        offers = result.get("result").get("offers")
        bids: Any = []
        asks: Any = []
        nonce = offers[-1].get("Sequence")

        for offer in offers:
            if offer.get("Flags") & 131072 == 0:
                if "value" in offer.get("TakerGets"):
                    bids.append([offer.get("quality"), offer.get("TakerGets").get("value")])
                else:
                    bids.append([offer.get("quality"), float(offer.get("TakerGets"))])
            else:
                if "value" in offer.get("TakerGets"):
                    asks.append([offer.get("quality"), offer.get("TakerGets").get("value")])
                else:
                    asks.append([offer.get("quality"), float(offer.get("TakerGets"))])

        return {
            "symbol": symbol,
            "nonce": nonce,
            "bids": bids,
            "asks": asks,
        }

    def fetch_trades(self, issuer: str) -> Dict:
        # book_offers
        payload = {
            "method": "book_offers",
            "params": [
                {
                    "taker_gets": {"currency": "XRP"},
                    "taker_pays": {"currency": "USD", "issuer": issuer},
                }
            ],
        }
        return self.json_rpc(payload)

    def transform_transactions(self, data: Any, extra: Any) -> Union[Dict, None]:
        if "transaction" in data:
            transaction = data.get("transaction")
            return data
        return None

    async def watch_transactions(self, listener: Callable, accounts: List) -> Dict:
        id = uuid.uuid4().hex
        payload = {
            "id": id,
            "command": "subscribe",
            "accounts": accounts,
        }
        extra = ()
        await self.subscribe(json.dumps(payload), listener, self.transform_transactions, extra)
        return {}

    def transform_my_trades(self, data: Any, extra: Any) -> Union[Dict, None]:
        if "transaction" in data:
            transaction = data.get("transaction")
            if transaction.get("TransactionType") == "Payment":
                return transaction
        return None

    async def watch_my_trades(self, listener: Callable, account: str) -> Dict:
        id = uuid.uuid4().hex
        payload = {
            "id": id,
            "command": "subscribe",
            "accounts": [account],
        }
        extra = ()
        await self.subscribe(json.dumps(payload), listener, self.transform_my_trades, extra)
        return {}

    def transform_balance(self, data: Any, extra: Any) -> Dict:
        (account) = extra
        if "meta" in data:
            meta = data.get("meta")
            if "AffectedNodes" in meta:
                affected_nodes = meta.get("AffectedNodes")
                for node in affected_nodes:
                    final = node.get("ModifiedNode").get("FinalFields")
                    if final.get("Account") == account:
                        return {"Account": account, "Balance": int(final.get("Balance")) / 1000000}
        return data

    async def watch_balance(self, listener: Callable, account: str) -> Dict:
        id = uuid.uuid4().hex
        payload = {
            "id": id,
            "command": "subscribe",
            "accounts": [account],
        }
        extra = (account,)
        await self.subscribe(json.dumps(payload), listener, self.transform_balance, extra)
        return {}

    def transform_create_order(self, data: Any, extra: Any) -> Dict:
        if "transaction" in data:
            transaction = data.get("transaction")
            if "TransactionType" in transaction:
                if transaction.get("TransactionType") == "OfferCreate":
                    return data
        return data

    async def watch_create_order(self, listener: Callable, account: str) -> Dict:
        id = uuid.uuid4().hex
        payload = {
            "id": id,
            "command": "subscribe",
            "accounts": [account],
        }
        extra = ()
        await self.subscribe(json.dumps(payload), listener, self.transform_create_order, extra)
        return {}

    def transform_cancel_order(self, data: Any, extra: Any) -> Union[Dict, None]:
        if "transaction" in data:
            transaction = data.get("transaction")
            if "TransactionType" in transaction:
                if transaction.get("TransactionType") == "OfferCancel":
                    return data
        return None

    async def watch_cancel_order(self, listener: Callable, account: str) -> Dict:
        id = uuid.uuid4().hex
        payload = {
            "id": id,
            "command": "subscribe",
            "accounts": [account],
        }
        extra = ()
        await self.subscribe(json.dumps(payload), listener, self.transform_cancel_order, extra)
        return {}

    def transform_orders(self, data: Any, extra: Any) -> Union[Dict, None]:
        (base, quote) = extra
        if "transaction" in data:
            transaction = data.get("transaction")
            if "TakerGets" in transaction and "TakerPays" in transaction:
                tg = data.get("transaction").get("TakerGets")
                tp = data.get("transaction").get("TakerPays")
                if "currency" in tg and "currency" in tp:
                    if tg.get("currency") == base and tp.get("currency") == quote:
                        return data
        return None

    async def watch_orders(self, listener: Callable, symbol: str) -> Dict:
        id = uuid.uuid4().hex
        [base, quote] = symbol.split("/")
        payload = {"id": id, "command": "subscribe", "streams": ["transactions"]}
        extra = (base, quote)
        await self.subscribe(json.dumps(payload), listener, self.transform_orders, extra)
        return {}

    def transform_trades(self, data: Any, extra: Any) -> Union[Dict, None]:
        (base, quote) = extra
        if "transaction" in data:
            transaction = data.get("transaction")
            if "TransactionType" in transaction and transaction.get("TransactionType") == "Payment":
                if "TakerGets" in transaction and "TakerPays" in transaction:
                    tg = data.get("transaction").get("TakerGets")
                    tp = data.get("transaction").get("TakerPays")
                    if "currency" in tg and "currency" in tp:
                        if tg.get("currency") == base and tp.get("currency") == quote:
                            return data
        return None

    async def watch_trades(self, listener: Callable, symbol: str) -> Dict:
        id = uuid.uuid4().hex
        [base, quote] = symbol.split("/")
        payload = {"id": id, "command": "subscribe", "streams": ["transactions"]}
        extra = (base, quote)
        await self.subscribe(json.dumps(payload), listener, self.transform_trades, extra)
        return {}

    def transform_tickers(self, data: Any, extra: Any) -> Union[Dict, None]:
        if "transaction" in data:
            transaction = data.get("transaction")
            # TODO: TRANSFORM to Price
            return {
                "TakerGets": transaction.get("TakerGets"),
                "TakerPays": transaction.get("TakerPays"),
            }
        return None

    async def watch_tickers(self, listener: Callable, symbols: list) -> Dict:
        markets: Any = self.fetch_markets()
        id = uuid.uuid4().hex
        payload: Any = {
            "id": id,
            "command": "subscribe",
            "books": [],
        }
        for symbol in symbols:
            if symbol not in markets:
                raise Exception("symbol not in markets")
            market: Any = markets.get(symbol)
            [base, quote] = symbol.split("/")
            taker_pays = {
                "currency": quote,
            }
            if "quoteIssuer" in market:
                taker_pays["issuer"] = market.get("quoteIssuer")
            taker_gets = {"currency": base}
            if "baseIssuer" in market:
                taker_gets["issuer"] = market.get("baseIssuer")
            payload.get("books").append({"taker_pays": taker_pays, "taker_gets": taker_gets})
        extra = ()
        await self.subscribe(json.dumps(payload), listener, self.transform_tickers, extra)
        return {}

    async def watch_ticker(self, listener: Callable, symbol: str) -> Dict:
        markets: Any = self.fetch_markets()
        if symbol not in markets:
            raise Exception("symbol not in markets")
        market: Any = markets.get(symbol)
        id = uuid.uuid4().hex
        [base, quote] = symbol.split("/")
        taker_pays = {
            "currency": quote,
        }
        if "quoteIssuer" in market:
            taker_pays["issuer"] = market.get("quoteIssuer")

        taker_gets = {"currency": base}
        if "baseIssuer" in market:
            taker_gets["issuer"] = market.get("baseIssuer")
        payload: Any = {
            "id": id,
            "command": "subscribe",
            "books": [{"taker_pays": taker_pays, "taker_gets": taker_gets}],
        }
        extra = ()
        await self.subscribe(json.dumps(payload), listener, self.transform_tickers, extra)
        return {}

    def transform_ledger(self, data: Any, extra: Any) -> Union[Dict, None]:
        return data

    async def watch_ledger(self, listener: Callable) -> Dict:
        id = uuid.uuid4().hex
        payload = {"id": id, "command": "subscribe", "streams": ["ledger"]}
        extra = ()
        await self.subscribe(json.dumps(payload), listener, self.transform_ledger, extra)
        return {}
