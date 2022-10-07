import json
from ..models.methods.fetch_transaction_fee import (
    FetchTransactionFeeResponse,
)


def fetch_transaction_fee(self, code: str) -> FetchTransactionFeeResponse:
    payload = {"method": "fee", "params": [{}]}
    fees_result = self.json_rpc(payload).get("result")

    currencies = self.fetch_currencies()
    if code in currencies is False:
        raise Exception("No code in currencies data")

    transfer_rates = {}

    currency = currencies.get(code)

    response = {
        "code": code,
        "current": int(fees_result.get("drops").get("open_ledger_fee")),
        "transfer": transfer_rates,
        "info": json.dumps({"feesResult": fees_result, "currency": currency}),
    }

    return response
