from typing import Optional
from ..models import LoadIssuersResponse


def load_issuers(self, reload: Optional[bool] = False) -> LoadIssuersResponse:
    """Retrieves and caches a list of issuers whose currencies are being traded on the dEX.

    Parameters
    ----------
    reload : bool
        (Optional) Whether to refresh the cache

    Returns
    -------
    xrpl_dex_sdk.models.LoadIssuersResponse
        The fetched issuers
    """

    if self.issuers == None or reload == True:
        issuers = self.fetch_issuers()
        self.issuers = issuers
    return self.issuers
