from typing import Union
from ..data import issuers_data
from ..models import Issuers


def fetch_issuers(self) -> Union[Issuers, None]:
    """Retrieves a list of currency issuers."""

    if self.issuers != None:
        return self.issuers

    if self.params.network == None:
        return

    issuers: Issuers = issuers_data[self.params.network]

    return issuers
