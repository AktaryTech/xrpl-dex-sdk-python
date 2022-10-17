from typing import Optional
from ..data import MarketsData
from ..models import FetchMarketsResponse


async def fetch_markets(self) -> Optional[FetchMarketsResponse]:
    if self.markets != None:
        return self.markets

    if self.network == None:
        return

    markets = MarketsData[self.network]

    if markets == None:
        return

    for market_symbol in markets:
        market = markets[market_symbol]
        if market == None:
            continue

        if market.base != "XRP":
            market.base_fee = await self.fetch_transfer_rate(market.base.issuer)
        if market.quote != "XRP":
            market.quote_fee = await self.fetch_transfer_rate(market.quote.issuer)

        markets[market_symbol] = market

    return markets
