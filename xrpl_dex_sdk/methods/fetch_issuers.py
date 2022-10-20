from ..data import IssuersData
from ..models import Issuers


def fetch_issuers(self) -> Issuers:
    if self.issuers != None:
        return self.issuers

    if self.network == None:
        return

    issuers: Issuers = IssuersData[self.network]

    return issuers
