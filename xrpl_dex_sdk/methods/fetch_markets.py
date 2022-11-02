from typing import Optional
from ..data import MarketsData
from ..models import CurrencyCode, MarketSymbol, FetchMarketsResponse, Market, Markets


async def fetch_markets(self) -> Optional[FetchMarketsResponse]:
    """Retrieves info about all markets being traded on the dEX."""

    if self.markets != None:
        return self.markets

    if self.params.network == None:
        return

    markets: Markets = {}

    network_markets = MarketsData[self.params.network]

    if network_markets == None:
        raise Exception(f"No markets list for network {self.params.network}!")

    for market_symbol in network_markets:
        market_data = network_markets[market_symbol]

        market = {
            "id": market_data["id"],
            "symbol": MarketSymbol.from_string(market_data["symbol"]),
            "base": CurrencyCode.from_string(market_data["base"]),
            "quote": CurrencyCode.from_string(market_data["quote"]),
        }

        if not market["base"].is_xrp():
            market["base_fee"] = await self.fetch_transfer_rate(market["base"].issuer)
        if not market["quote"].is_xrp():
            market["quote_fee"] = await self.fetch_transfer_rate(market["quote"].issuer)

        markets[market["symbol"]] = Market.from_dict(market)

    return markets
