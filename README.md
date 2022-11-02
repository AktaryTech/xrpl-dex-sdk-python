# XRPL Decentralized Exchange SDK

This Python SDK provides a [CCXT-compatible API](https://docs.ccxt.com/en/latest/manual.html?#unified-api) for interacting with the [XRPL decentralized exchange](https://xrpl.org/decentralized-exchange.html).

A TypeScript version of this SDK is available [here](https://github.com/AktaryTech/xrpl-dex-sdk).

## Installation

This package requires [Python v3.8](https://www.python.org/downloads/release/python-3810) (or newer) and the [Pip](https://pypi.org/project/pip/) package installer.

### From PyPI

1. Add the SDK as a dependency to your project:

```
$ pip install xrpl_dex_sdk
```

2. Import the SDK into your script:

```python
import xrpl_dex_sdk
```

### From Source

1. Make sure you have [Poetry](https://python-poetry.org/docs/) installed on your system.

> NOTE: If you use VSCode, it should automatically show a prompt to select the virtual environment created by Poetry (`./.venv`). You will now have auto-formatting with `black`, linting with `flake8`, type-checking with `mypy`, and vscode testing configs.

2. Clone the repo and install dependencies:

```
$ git clone https://github.com/AktaryTech/xrpl-dex-sdk-python.git
$ cd xrpl-dex-sdk-python
$ poetry install
```

## Usage

To use the SDK, import it into your script and initialize it:

```python
from xrpl_dex_sdk import SDK, SDKParams, constants

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
| MarketSymbol     | `[BaseCurrency]/[QuoteCurrency]` | `XRP/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq`  |
| OrderId, TradeId | `[AccountAddress]/[Sequence]`    | `rpkeJcxB2y5BeAFyycuWwdTTcR3og2a3SR:30419065` |

### Examples

#### Placing an Order

The following example places an Order to buy 20 TST tokens, issued by the account at `rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd`, at a price of 1.5 XRP each:

```python
from xrpl_dex_sdk import SDK, SDKParams, constants, models

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

```
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
from xrpl_dex_sdk import SDK, SDKParams, constants, models

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

For full SDK documentation, load [`docs/_build/html/index.html`](docs/_build/html/index.html) in your browser. Run `docs/build.sh` to re-generate documentation.

## Further Reading

### CCXT (CryptoCurrency eXchange Trading Library)

- [General Documentation](https://docs.ccxt.com/en/latest/index.html)
- [Unified API](https://docs.ccxt.com/en/latest/manual.html#unified-api)

### XRPL Ledger

- [General Documentation](https://xrpl.org/concepts.html)
- [Decentralized Exchange](https://xrpl.org/decentralized-exchange.html)
- [dEX Tutorial](https://xrpl.org/trade-in-the-decentralized-exchange.html)

## Contributing

Pull requests, issues and comments are welcome! Make sure to add tests for new features and bug fixes.

## Contact

For questions, suggestions, etc, you can reach the maintainer at [info@aktarytech.com](mailto:info@aktarytech.com).

## License

The software is distributed under the MIT license. See [LICENSE](https://github.com/AktaryTech/xrpl-dex-sdk-python/blob/main/LICENSE) for details.

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in this library by you, as defined in the MIT license, shall be licensed as above, without any additional terms or conditions.

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Copyright

Copyright © 2022 Ripple Labs, Inc.
