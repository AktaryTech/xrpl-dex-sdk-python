from typing import Union
from ..data import IssuersData
from ..models import Issuers


def fetch_issuers(self) -> Union[Issuers, None]:
    """Retrieves a list of currency issuers."""

    if self.issuers != None:
        return self.issuers

    if self.params.network == None:
        return

    issuers: Issuers = IssuersData[self.params.network]

    return issuers
