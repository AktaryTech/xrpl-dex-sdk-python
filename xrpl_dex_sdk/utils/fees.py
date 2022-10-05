import json

from xrpl.clients import JsonRpcClient
from xrpl.models.requests.account_info import AccountInfo

from ..models.xrpl import Amount
from ..utils.conversions import transfer_rate_to_decimal


async def fetch_transfer_rate(client: JsonRpcClient, amount: Amount) -> float:
    issuer = amount.issuer
    if issuer != None:
        account_info_request = AccountInfo.from_dict(
            {"account": issuer, "ledger_index": "validated"}
        )
        account_info_response = await client.request(account_info_request)
        account_info_result = account_info_response.result

        if account_info_result != None:
            account_info = account_info_result
            # account_info = json.dumps(account_info_result.node, indent=4, sort_keys=True)
            if account_info.account_data.TransferRate:
                return transfer_rate_to_decimal(account_info.account_data.TransferRate)

    return 0
