from typing import List
from ..models import CurrencyCode, FetchTransactionFeesResponse


async def fetch_transaction_fees(
    self, codes: List[CurrencyCode]
) -> FetchTransactionFeesResponse:
    """
    Returns information about fees incurred for performing transactions with any currency.

    Parameters
    ----------
    codes : List[CurrencyCode]
        List of currency codes to get fees for

    Returns
    -------
    FetchTransactionFeesResponse
        Transaction fees data
    """

    transaction_fees: FetchTransactionFeesResponse = []

    for code in codes:
        transaction_fee = await self.fetch_transaction_fee(code)
        if transaction_fee != None:
            transaction_fees.append(transaction_fee)

    return transaction_fees
