from typing import Any, Dict

from ..models.methods.fetch_balance import FetchBalanceParams, FetchBalanceResponse
from ..models.ccxt.balances import Balance
from ..utils.conversions import drops_to_xrp


def fetch_balance(self, params: FetchBalanceParams) -> FetchBalanceResponse:
    balances: Dict[str, Balance] = {}
    info: Dict[str, Any] = {}

    # get XRP balance
    if "code" not in params or params["code"] == "XRP":
        account_info_request = {
            "method": "account_info",
            "params": [
                {
                    "account": params["account"],
                    "strict": True,
                    "ledger_index": "validated",
                    "queue": False,
                }
            ],
        }
        account_info_response = self.json_rpc(account_info_request)
        account_info = account_info_response["result"]["account_data"]
        account_object_count = account_info["OwnerCount"]

        server_state_request = {"method": "server_state", "params": [{}]}
        server_state_response = self.json_rpc(server_state_request)

        validated_ledger = server_state_response["result"]["state"]["validated_ledger"]
        xrp_reserve_base = drops_to_xrp(validated_ledger["reserve_base"])
        xrp_reserve_inc = drops_to_xrp(validated_ledger["reserve_inc"])

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
            account_lines_request = {
                "method": "account_lines",
                "params": [
                    {
                        "account": params["account"],
                    }
                ],
            }
            account_lines_response = self.json_rpc(account_lines_request)

            trust_lines = account_lines_response["result"]["lines"]

            for trust_line in trust_lines:
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

            marker = account_lines_response["result"]["marker"]
            has_next_page = marker != None

    return {"balances": balances, "info": info}
