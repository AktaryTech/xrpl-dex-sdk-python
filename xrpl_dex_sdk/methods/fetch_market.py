from ..data import MarketsData
from ..models import MarketSymbol, FetchMarketResponse, CurrencyCode, Markets
from ..utils import fetch_transfer_rate


def fetch_market(self, symbol: MarketSymbol) -> FetchMarketResponse:
    if self.markets != None and symbol.symbol in self.markets:
        return self.markets[symbol.symbol]

    if self.network == None:
        return

    markets: Markets = MarketsData[self.network]

    if symbol.symbol not in markets:
        return

    market = markets[symbol.symbol]

    if market == None:
        return

    if market["base"] != "XRP":
        [code, issuer] = market["base"].split("+")
        market["base_fee"] = fetch_transfer_rate(
            self.client, CurrencyCode(code, issuer)
        )
    if market["quote"] != "XRP":
        [code, issuer] = market["quote"].split("+")
        market["quote_fee"] = fetch_transfer_rate(
            self.client, CurrencyCode(code, issuer)
        )

    return market
