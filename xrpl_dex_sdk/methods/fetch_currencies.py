from ..data import CurrenciesData
from ..models import Currencies


async def fetch_currencies(self) -> Currencies:
    if self.currencies != None:
        return self.currencies

    if self.network == None:
        return

    currencies: Currencies = CurrenciesData[self.network]

    if currencies == None:
        return

    for currency in currencies:
        if "issuer" in currency:
            fee_rate = await self.fetch_transfer_rate(currency.issuer)
            if fee_rate != 0:
                currencies[currency].fee = fee_rate

    return currencies
