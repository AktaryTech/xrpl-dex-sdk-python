from typing import Optional
from ..models import LoadCurrenciesResponse


async def load_currencies(self, reload: Optional[bool] = False) -> LoadCurrenciesResponse:
    if self.currencies == None or reload == True:
        currencies = await self.fetch_currencies()
        self.currencies = currencies
    return self.currencies
