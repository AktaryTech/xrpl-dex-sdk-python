import json
from pprint import pprint

from xrpl.clients import JsonRpcClient
from xrpl.models.requests.account_info import AccountInfo

from ..constants import BILLION
from ..models import Amount
from ..utils.conversions import transfer_rate_to_decimal


def fetch_transfer_rate(client: JsonRpcClient, amount: Amount) -> float:
    if isinstance(amount, str):
        return float(0)

    issuer = amount["issuer"]
    if issuer != None:
        account_info_request = AccountInfo.from_dict(
            {"account": issuer, "ledger_index": "validated"}
        )
        account_info_response = client.request(account_info_request)
        if account_info_response.__getattribute__("result") != None:
            account_info_result = account_info_response.result
            if account_info_result["account_data"]["TransferRate"]:
                transfer_rate = transfer_rate_to_decimal(
                    account_info_result["account_data"]["TransferRate"]
                )
                return transfer_rate

    return float(0)
