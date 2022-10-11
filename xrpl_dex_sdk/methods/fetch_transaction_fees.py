from typing import List
from ..models.methods.fetch_transaction_fees import FetchTransactionFeesResponse
from ..models.common import CurrencyCode


def fetch_transaction_fees(
    self, codes: List[CurrencyCode]
) -> FetchTransactionFeesResponse:
    transaction_fees: FetchTransactionFeesResponse = []

    for code in codes:
        transaction_fee = self.fetch_transaction_fee(code)
        if transaction_fee != None:
            transaction_fees.append(transaction_fee)

    return transaction_fees
