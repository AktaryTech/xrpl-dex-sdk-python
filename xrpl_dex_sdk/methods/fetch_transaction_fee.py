from typing import Optional, Union
from xrpl.models.requests.fee import Fee

from ..models import FetchTransactionFeeResponse, CurrencyCode, TransactionFee
from ..utils import handle_response_error


async def fetch_transaction_fee(
    self, code: Union[CurrencyCode, str]
) -> Optional[FetchTransactionFeeResponse]:
    code = CurrencyCode.from_string(code) if isinstance(code, str) else code

    fee_response = await self.client.request(Fee())
    fee_result = fee_response.result
    handle_response_error(fee_result)

    currencies = self.currencies if self.currencies != None else await self.fetch_currencies()

    print(await self.fetch_currencies())

    if code not in currencies:
        return

    return TransactionFee(
        code=code,
        current=fee_result["drops"]["open_ledger_fee"],
        transfer=currencies[code].fee,
        info={"fee": fee_result, "currency": currencies[code]},
    )
