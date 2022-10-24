# XRPL Decentralized Exchange SDK

This Python SDK provides a [CCXT-compatible API](https://docs.ccxt.com/en/latest/manual.html?#unified-api) for interacting with the [XRPL decentralized exchange](https://xrpl.org/decentralized-exchange.html).

A TypeScript version of this SDK is available [here]().

## Getting Started

### Prerequisites

Make sure you have the following installed on your system:

- Python v3.6+
- [Poetry](https://python-poetry.org/docs/)

### Visual Studio Code (Optional)

If you use VSCode, it should automatically show a prompt to select the virtual environment created by Poetry (`./.venv`). You will now have auto-formatting with `black`, linting with `flake8`, type-checking with `mypy`, and vscode testing configs.

### Installation

Add the SDK as a dependency in your app:

```
$ poetry add xrpl_dex_sdk_python
```

#### From Source

```
$ git clone https://github.com/[ORG_LINK_HERE]/xrpl-dex-sdk-python.git
$ cd xrpl-dex-sdk-python
$ poetry install
```

## Usage

To use the SDK, import it into your script and initialize it:

```python
from xrpl_dex_sdk_python import SDK, SDKParams, constants

sdk = SDK(SDKParams.from_dict({
  "network": constants.TESTNET,
  "generate_wallet": True,
}))
```

### Currencies, MarketSymbols, and ID Formatting

Currency codes, market symbols (aka pairs), and Order/Trade IDs are strings that follow the following formats:

| Type             | Format                           | Example                                       |
| ---------------- | -------------------------------- | --------------------------------------------- |
| CurrencyCode     | `[Currency]+[IssuerAddress]`     | `USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq`      |
| MarketSymbol     | `[BaseCurrency]/[QuoteCurrency]` | `USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq/XRP`  |
| OrderId, TradeId | `[AccountAddress]/[Sequence]`    | `rpkeJcxB2y5BeAFyycuWwdTTcR3og2a3SR:30419065` |

### Examples

#### Placing an Order

The following example places an Order to buy 20 TST tokens, issued by the wallet at `rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd`, at a price of 1.5 XRP each:

```python
from xrpl_dex_sdk_python import SDK, SDKParams, constants, models

sdk = SDK(SDKParams(
  network=constants.TESTNET,
  generate_wallet=True,
))

create_order_result = await sdk.create_order(
    symbol="TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",
    side=models.OrderSide.Buy,
    type=models.OrderType.Limit,
    amount=20,
    price=1.5,
)

order = await sdk.fetch_order(create_order_result.id)

print(order)
```

Outputs the newly created Order object:

```json
{
  ...,
  "status": "open",
  "symbol": "TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",
  "type": "limit",
  "timeInForce": "GTC",
  "side": "buy",
  "amount": "20",
  "price": "1.5",
  "average": "0",
  "filled": "0",
  "remaining": "20",
  "cost": "0",
  "trades": [],
  "info": {
    // ... raw response from XRPL server
  }
}
```

#### Fetching an Order Book

The following example retrieves the latest order book for the market pair `TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP`:

```python
from xrpl_dex_sdk_python import SDK, SDKParams, constants, models

sdk = SDK(SDKParams(
  network=constants.TESTNET,
  generate_wallet=True,
))

order_book = await sdk.fetch_order_book(
    symbol="TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",
    limit=5
)

print(order_book)
```

Outputs an object like the following:

```json
{
  "symbol": "TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",
  "bids": [
    ["0.0030627837459923", "93.030522464522"],
    ["0.00302447007930511", "1"]
  ],
  "asks": [["331.133829801611", "0.3"]],
  "info": {
    // ... raw response from XRPL server
  }
}
```

## Methods

See the full SDK documentation here, or run `!!! Python generate docs command here !!!` to generate the documentation locally.

## Further Reading

### CCXT (CryptoCurrency eXchange Trading Library)

- General Documentation - https://docs.ccxt.com/en/latest/index.html
- Unified API - https://docs.ccxt.com/en/latest/manual.html#unified-api

### XRPL Ledger

- General Documentation
- Decentralized Exchange
