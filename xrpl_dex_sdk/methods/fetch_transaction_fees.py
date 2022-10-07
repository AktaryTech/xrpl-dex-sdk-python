from typing import List

from ..models.common import CurrencyCode
from ..models.methods.fetch_transaction_fees import (
    FetchTransactionFeesResponse,
)


def fetch_transaction_fees(
    self, codes: List[CurrencyCode]
) -> FetchTransactionFeesResponse:
    response: list = []
    for code in codes:
        response.append(self.fetch_transaction_fee(code))
    return response
