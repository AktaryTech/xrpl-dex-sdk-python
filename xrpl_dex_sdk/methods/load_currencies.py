from typing import Optional
from ..models import LoadCurrenciesResponse


async def load_currencies(self, reload: Optional[bool] = False) -> LoadCurrenciesResponse:
    """
    Retrieves and caches a list of currencies being traded on the dEX.

    Parameters
    ----------
    reload : bool
        (Optional) Whether to refresh the cache

    Returns
    -------
    xrpl_dex_sdk.models.LoadCurrenciesResponse
        The fetched currencies
    """

    if self.currencies == None or reload == True:
        currencies = await self.fetch_currencies()
        self.currencies = currencies
    return self.currencies
