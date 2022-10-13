from ..data import MarketsData
from ..models import FetchMarketsResponse, CurrencyCode


async def fetch_markets(self) -> FetchMarketsResponse:
    if self.markets != None:
        return self.markets

    if self.network == None:
        return

    markets = MarketsData[self.network]

    if markets == None:
        return

    for market in markets:
        if markets[market]["base"] != "XRP":
            markets[market]["base_fee"] = await self.fetch_transfer_rate(
                CurrencyCode(markets[market]["base"]).issuer
            )
        if markets[market]["quote"] != "XRP":
            markets[market]["quote_fee"] = await self.fetch_transfer_rate(
                CurrencyCode(markets[market]["quote"]).issuer
            )

    return markets
