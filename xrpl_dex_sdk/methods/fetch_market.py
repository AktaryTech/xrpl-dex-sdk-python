from ..data import MarketsData
from ..models import MarketSymbol, FetchMarketResponse, CurrencyCode, Market


async def fetch_market(self, symbol: MarketSymbol) -> FetchMarketResponse:
    symbol = MarketSymbol(symbol) if isinstance(symbol, str) == True else symbol

    if self.markets != None and symbol.symbol in self.markets:
        return self.markets[symbol.symbol]

    market: Market = None

    if self.network != None:
        if self.network in MarketsData and symbol.symbol in MarketsData[self.network]:
            market = MarketsData[self.network][symbol.symbol]
    else:
        for network_markets in MarketsData:
            if symbol.symbol in network_markets:
                market = network_markets[symbol.symbol]

    if market == None:
        return

    if market["base"] != "XRP":
        market["base_fee"] = await self.fetch_transfer_rate(
            CurrencyCode(market["base"]).issuer
        )
    if market["quote"] != "XRP":
        market["quote_fee"] = await self.fetch_transfer_rate(
            CurrencyCode(market["quote"]).issuer
        )

    return market
