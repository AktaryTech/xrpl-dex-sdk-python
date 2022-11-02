from ..data import CurrenciesData
from ..models import Currency, CurrencyCode, Currencies


async def fetch_currencies(self) -> Currencies:
    """Retrieves a list of currencies being traded on the dEX."""

    if self.currencies != None:
        return self.currencies

    if self.params.network == None:
        raise Exception("No network param set on SDK instance!")

    currencies: Currencies = {}

    network_currencies = CurrenciesData[self.params.network]

    if network_currencies == None:
        raise Exception(f"No currency list for network {self.params.network}!")

    for currency_name in network_currencies:
        currency_data = network_currencies[currency_name]

        currency = {
            "code": CurrencyCode.from_string(currency_data["code"]),
            "name": currency_data["name"],
            "issuer_name": currency_data["issuer_name"],
            "logo": currency_data["logo"] if "logo" in currency_data else None,
            "precision": currency_data["precision"] if "precision" in currency_data else None,
        }

        fee_rate = await self.fetch_transfer_rate(currency["code"].issuer)
        if fee_rate != 0:
            currency["fee"] = fee_rate
        currencies[currency["code"]] = Currency.from_dict(currency)

    return currencies
