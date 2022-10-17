from typing import Optional
from xrpl.models.requests.fee import Fee

from ..models.methods.fetch_transaction_fee import FetchTransactionFeeResponse
from ..models.common import CurrencyCode
from ..models.ccxt import TransactionFee


async def fetch_transaction_fee(
    self, code: CurrencyCode
) -> Optional[FetchTransactionFeeResponse]:
    fee_response = await self.client.request(Fee())
    fee_result = fee_response.result

    if "error" in fee_result:
        raise Exception(fee_response["error"] + " " + fee_response["error_message"])

    currencies = (
        self.currencies if self.currencies != None else await self.fetch_currencies()
    )

    if code not in currencies:
        return

    return TransactionFee(
        code=code,
        current=fee_result["drops"]["open_ledger_fee"],
        transfer=currencies[code].get("fee", 0),
        info={"fee": fee_result, "currency": currencies[code]},
    )
