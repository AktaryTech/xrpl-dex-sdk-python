from ..models.methods.fetch_currencies import FetchCurrenciesResponse


def fetch_currencies(self) -> FetchCurrenciesResponse:
    if "fetch_currencies" in self._cache:
        return self._cache.get("fetch_currencies")
    currencies = self.load_data("currencies.json")
    for _, currency in currencies.items():
        for curr in currency:
            payload = {"method": "account_info", "params": [{"account": curr.get("issuer")}]}
            account_info_result = self.json_rpc(payload).get("result")
            account_rate = account_info_result.get("account_data").get("TransferRate")
            if account_rate:
                curr["fee"] = self.transfer_rate_to_decimal(account_rate)
    self._cache["fetch_currencies"] = currencies
    return currencies
