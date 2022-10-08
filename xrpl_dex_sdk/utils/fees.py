from xrpl.clients import JsonRpcClient
from xrpl.models.requests.account_info import AccountInfo

from ..models import CurrencyCode
from ..utils.conversions import transfer_rate_to_decimal


def fetch_transfer_rate(client: JsonRpcClient, currency_code: CurrencyCode) -> float:
    if currency_code.issuer == None:
        return 0

    account_info_request = AccountInfo.from_dict(
        {"account": currency_code.issuer, "ledger_index": "validated"}
    )
    account_info_response = client.request(account_info_request)
    account_info_result = account_info_response.result
    if account_info_result != None:
        if "TransferRate" in account_info_result["account_data"]:
            transfer_rate = transfer_rate_to_decimal(
                account_info_result["account_data"]["TransferRate"]
            )
            return transfer_rate

    return 0
