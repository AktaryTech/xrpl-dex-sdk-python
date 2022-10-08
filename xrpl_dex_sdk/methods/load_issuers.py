from typing import Optional
from ..models import LoadIssuersResponse


def load_issuers(self, reload: Optional[bool] = False) -> LoadIssuersResponse:
    if self.issuers == None or reload == True:
        issuers = self.fetch_issuers()
        self.issuers = issuers
    return self.issuers
