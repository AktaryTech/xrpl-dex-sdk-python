# import asyncio
# import json
# from typing import Any
# from uuid import uuid4

# from xrpl_dex_sdk import constants, models, SDK

# # client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
# # client = xrpl_dex_sdk.Client(xrpl_dex_sdk.MAINNET)

# # print(client.fetch_status())
# # print(client.fetch_currencies())
# # print(client.fetch_markets())
# # print(client.fetch_issuers())
# # print(client.fetch_balance("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"))
# # print(
# #     client.fetch_order_book(
# #         "XRP/USD",
# #         3,
# #         {
# #             "taker": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
# #             "taker_pays_issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
# #         },
# #     )
# # )

# # print(
# #     client.fetch_order_books(
# #         ["XRP/USD"],
# #         3,
# #         {
# #             "XRP/USD": {
# #                 "taker": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
# #                 "taker_pays_issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
# #             },
# #         },
# #     )
# # )
# # print(client.fetch_trading_fee("XRP/USD"))
# # print(client.fetch_trading_fees())
# # print(client.fetch_transaction_fee("EUR"))
# # print(client.fetch_transaction_fees(["EUR", "USD"]))
# # print(client.fetch_fees())


# # def foo(data: Any) -> None:
# #     print(json.dumps(data, indent=4))


# # def write_to_out(data: Any) -> None:

# #     f = open("./out/" + uuid4().hex, "w")
# #     f.write(json.dumps(data, indent=4))
# #     f.close()


# def main() -> None:
#     # client = xrpl_dex_sdk.Client(xrpl_dex_sdk.TESTNET)
#     # sdk = SDK(
#     #     {
#     #         "network": constants.TESTNET,
#     #         "wallet_secret": "shCwGCyy17Ph4JdZ6jTsFssEpS6Fs",
#     #     }
#     # )

#     # balance_data = {"free": 2.5, "used": 1.25, "total": 3.75}
#     # balance = models.Balance.from_dict(balance_data)
#     # print("Got balance:\n")
#     # print(balance)

#     # await sdk.watch_balance(foo)
#     # await client.watch_status(foo)
#     # await client.watch_order_book(foo, "XRP/EUR")
#     # await client.watch_transactions(foo, ["rJ9D95MwHFHxDDyeBg4SG644wPYqyEGsE7"])
#     # await client.watch_my_trades(foo, "rhLSGdavS2B3NVDQX23rQ9zaRrBcKb96BP")
#     # await client.watch_balance(foo, "rhLSGdavS2B3NVDQX23rQ9zaRrBcKb96BP")
#     # await client.watch_create_order(foo, "rhvXHRpiWhuXAztZiz3f4AgVr3jwPmNmVv")
#     # await client.watch_cancel_order(foo, "rhvXHRpiWhuXAztZiz3f4AgVr3jwPmNmVv")
#     # await client.watch_orders(write_to_out, "EUR/USD")
#     # await client.watch_trades(write_to_out, "EUR/USD")
#     # await client.watch_ticker(foo, "XRP/EUR")
#     # await client.watch_tickers(foo, ["XRP/EUR", "XRP/USD", "XRP/ETH", "BTC/USD"])
#     # await client.watch_ledger(foo)


# # asyncio.run(main())
# # main()

# # RAW
# # print(client.fetch_trades("r41R8dEUQgFvkMnwcDKQ1bC3ty6L1pNfib"))

from dataclasses import dataclass
from typing import (
    Dict,
    Optional,
)
from xrpl_dex_sdk.constants import ISO_CURRENCY_REGEX, HEX_CURRENCY_REGEX
from xrpl_dex_sdk.models import BaseModel, REQUIRED


@dataclass(frozen=True)
class CurrencyCode(BaseModel):
    currency: str = REQUIRED
    issuer: Optional[str] = None

    # @classmethod
    # def from_str(cls, code_str: str):
    #     [currency, *issuer] = code_str.split("+")
    #     code_dict = {"currency": currency}
    #     if len(issuer) > 0:
    #         code_dict["issuer"] = issuer[0]
    #     return cls.from_dict(code_dict)

    def _get_errors(self: "CurrencyCode") -> Dict[str, str]:
        errors = super()._get_errors()
        if self.currency.upper() == "XRP" and self.issuer != None:
            errors["currency"] = "XRP does not require an Issuer"
        elif not self._is_valid_currency(self.currency):
            errors["currency"] = f"Invalid currency: {self.currency}"
        return errors

    def _is_valid_currency(self, value: str) -> bool:
        return bool(ISO_CURRENCY_REGEX.fullmatch(value) or HEX_CURRENCY_REGEX.fullmatch(value))

    def _get_code(self) -> str:
        return self.currency + ("+" + self.issuer if self.issuer != None else "")

    # def __init__(self, code: str, issuer: Optional[str] = None) -> None:
    #     if isinstance(code, str) == False:
    #         raise Exception(
    #             "Error creating CurrencyCode: provided value is not a string"
    #         )
    #     currency_issuer_pair = [code, issuer] if issuer != None else code.split("+")
    #     if currency_issuer_pair[0] == None:
    #         raise Exception(
    #             "Error creating CurrencyCode: " + code + " is not a valid code"
    #         )
    #     self.currency = currency_issuer_pair[0]
    #     self.issuer = (
    #         currency_issuer_pair[1] if len(currency_issuer_pair) == 2 else None
    #     )
    #     self.code = self.currency
    #     if self.issuer != None:
    #         self.code += "+" + self.issuer

    # def __repr__(self) -> str:
    #     return self._get_code()

    def __str__(self) -> str:
        return self._get_code()


def main() -> None:
    code = CurrencyCode.from_dict({"currency": "USD", "issuer": "r12345"})

    print("\n Code")
    print(code)
    print(code.to_json())
    print(isinstance(code.to_json(), str))
    print("\n")


main()
