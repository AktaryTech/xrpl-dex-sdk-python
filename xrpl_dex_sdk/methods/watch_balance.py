from typing import Any, Dict, Optional

from xrpl.models.requests.account_info import AccountInfo
from xrpl.models.requests.account_lines import AccountLines
from xrpl.models.requests.server_state import ServerState
from xrpl.utils import drops_to_xrp

from ..models import WatchBalanceParams, WatchBalanceResponse, Balance


def watch_balance(self, params: Optional[WatchBalanceParams] = {}) -> WatchBalanceResponse:
    balances: Dict[str, Balance] = {}
    info: Dict[str, Any] = {}

    # get XRP balance
    if "code" not in params or params["code"] == "XRP":
        account_info_response = self.client.request(
            AccountInfo.from_dict(
                {"account": self.wallet.classic_address, "ledger_index": "validated"}
            )
        )
        account_info_result = account_info_response.result
        account_info = account_info_result["account_data"]
        account_object_count = account_info["OwnerCount"]

        server_state_response = self.client.request(ServerState())
        server_state_result = server_state_response.result

        validated_ledger = server_state_result["state"]["validated_ledger"]
        xrp_reserve_base = drops_to_xrp(str(validated_ledger["reserve_base"]))
        xrp_reserve_inc = drops_to_xrp(str(validated_ledger["reserve_inc"]))

        used_xrp = xrp_reserve_base + account_object_count * xrp_reserve_inc
        free_xrp = drops_to_xrp(account_info["Balance"]) - used_xrp
        total_xrp = used_xrp + free_xrp

        balances["XRP"] = {"free": free_xrp, "used": used_xrp, "total": total_xrp}

        info["account_info"] = account_info
        info["validated_ledger"] = validated_ledger

    # get token balances
    else:
        marker: Any
        has_next_page = True

        while has_next_page == True:
            account_lines_response = self.client.request(
                AccountLines.from_dict({"account": self.wallet.classic_address})
            )
            account_lines_result = account_lines_response.result

            for trust_line in account_lines_result["lines"]:
                currency_code = trust_line.currency + "+" + trust_line["account"]

                if "code" in params and currency_code != params["code"]:
                    continue

                used_balance = 0
                free_balance = trust_line["balance"] - used_balance
                total_balance = used_balance + free_balance

                balances[currency_code] = {
                    "free": free_balance,
                    "used": used_balance,
                    "total": total_balance,
                }

            info["account_lines"] = account_lines_response

            marker = account_lines_result["marker"]
            has_next_page = marker != None

    return {"balances": balances, "info": info}
