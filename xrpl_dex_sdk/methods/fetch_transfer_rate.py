from xrpl.models import AccountInfo
from ..models import IssuerAddress
from ..utils import handle_response_error, transfer_rate_to_decimal


async def fetch_transfer_rate(self, issuer: IssuerAddress) -> float:
    """
    Retrieves a currency issuer's transfer rate (if any).

    Parameters
    ----------
    issuer : xrpl_dex_sdk.models.IssuerAddress
        Address of currency issuer

    Returns
    -------
    float
        The transfer rate
    """

    if self.transfer_rates != None and "issuer" in self.transfer_rates:
        return self.transfer_rates[issuer]
    account_info_request = AccountInfo.from_dict({"account": issuer, "ledger_index": "validated"})
    account_info_response = await self.client.request(account_info_request)
    account_info_result = account_info_response.result
    handle_response_error(account_info_result)

    if account_info_result != None:
        if "TransferRate" in account_info_result["account_data"]:
            transfer_rate = transfer_rate_to_decimal(
                account_info_result["account_data"]["TransferRate"]
            )
            if transfer_rate != None:
                if self.transfer_rates == None:
                    self.transfer_rates = {}
                self.transfer_rates[issuer] = transfer_rate
                return transfer_rate

    return float(0)
