from ..data import MarketsData
from ..models import FetchMarketsResponse, CurrencyCode
from ..utils import fetch_transfer_rate


def fetch_markets(self) -> FetchMarketsResponse:
    if self.markets != None:
        return self.markets

    if self.network == None:
        return

    markets = MarketsData[self.network]

    if markets == None:
        return

    for market in markets:
        if markets[market]["base"] != "XRP":
            [code, issuer] = markets[market]["base"].split("+")
            markets[market]["base_fee"] = fetch_transfer_rate(
                self.client, CurrencyCode(code, issuer)
            )
        if markets[market]["quote"] != "XRP":
            [code, issuer] = markets[market]["quote"].split("+")
            markets[market]["quote_fee"] = fetch_transfer_rate(
                self.client, CurrencyCode(code, issuer)
            )

    return markets
