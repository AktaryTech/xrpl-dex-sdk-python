from typing import Any, Dict, Optional

from xrpl.models.requests.account_info import AccountInfo
from xrpl.models.requests.account_lines import AccountLines
from xrpl.models.requests.server_state import ServerState
from xrpl.utils import drops_to_xrp

from ..models import CurrencyCode, FetchBalanceParams, FetchBalanceResponse, Balance
from ..utils import handle_response_error


async def fetch_balance(
    self, params: Optional[FetchBalanceParams] = FetchBalanceParams()
) -> Optional[FetchBalanceResponse]:
    """
    Returns information about an account's balances.

    Results are sorted by currency and funds availability.

    Parameters
    ----------
    params : xrpl_dex_sdk.models.FetchBalanceParams
        (Optional) Additional request parameters

    Returns
    -------
    xrpl_dex_sdk.models.FetchBalanceResponse
        Balance information
    """

    balances: Dict[CurrencyCode, Balance] = {}
    info: dict = {}

    # get XRP balance
    if getattr(params, "code") == None or getattr(params, "code") == "XRP":
        account_info_response = await self.client.request(
            AccountInfo.from_dict(
                {"account": self.wallet.classic_address, "ledger_index": "validated"}
            )
        )
        account_info_result = account_info_response.result
        handle_response_error(account_info_result)

        account_info = account_info_result["account_data"]
        account_object_count = account_info["OwnerCount"]

        server_state_response = await self.client.request(ServerState())
        server_state_result = server_state_response.result
        handle_response_error(server_state_result)

        validated_ledger = server_state_result["state"]["validated_ledger"]
        xrp_reserve_base = float(drops_to_xrp(str(validated_ledger["reserve_base"])))
        xrp_reserve_inc = float(drops_to_xrp(str(validated_ledger["reserve_inc"])))

        used_xrp = xrp_reserve_base + account_object_count * xrp_reserve_inc
        free_xrp = float(drops_to_xrp(account_info["Balance"])) - used_xrp
        total_xrp = used_xrp + free_xrp

        balances[CurrencyCode("XRP")] = Balance(free=free_xrp, used=used_xrp, total=total_xrp)

        info["account_info"] = account_info
        info["validated_ledger"] = validated_ledger

    # get token balances
    else:
        marker: Any
        has_next_page = True

        while has_next_page == True:
            account_lines_response = await self.client.request(
                AccountLines.from_dict({"account": self.wallet.classic_address})
            )
            account_lines_result = account_lines_response.result
            handle_response_error(account_lines_result)

            for trust_line in account_lines_result["lines"]:
                currency_code = CurrencyCode(trust_line.currency, trust_line["account"])

                if getattr(params, "code") != currency_code:
                    continue

                used_balance = 0
                free_balance = trust_line["balance"] - used_balance
                total_balance = used_balance + free_balance

                balances[currency_code] = Balance(
                    free=free_balance,
                    used=used_balance,
                    total=total_balance,
                )

            info["account_lines"] = account_lines_response

            marker = account_lines_result["marker"]
            has_next_page = marker != None

    return FetchBalanceResponse(balances=balances, info=info)
