from typing import Optional
from ..models import Markets


async def load_markets(self, reload: Optional[bool] = False) -> Markets:
    """
    Retrieves and caches a list of markets being traded on the dEX.

    Parameters
    ----------
    reload : bool
        (Optional) Whether to refresh the cache

    Returns
    -------
    xrpl_dex_sdk.models.LoadMarketsResponse
        The fetched markets
    """

    if self.markets == None or reload == True:
        markets = await self.fetch_markets()
        self.markets = markets
    return self.markets
