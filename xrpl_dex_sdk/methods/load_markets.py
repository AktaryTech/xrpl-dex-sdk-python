from typing import Optional
from ..models import Markets


def load_markets(self, reload: Optional[bool] = False) -> Markets:
    if self.markets == None or reload == True:
        markets = self.fetch_markets()
        self.markets = markets
    return self.markets
