from typing import Union
from ..data import IssuersData
from ..models import Issuers


def fetch_issuers(self) -> Union[Issuers, None]:
    if self.issuers != None:
        return self.issuers

    if self.network == None:
        return

    issuers: Issuers = IssuersData[self.network]

    return issuers
