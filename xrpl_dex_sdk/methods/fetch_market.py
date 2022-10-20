from typing import Optional, Union
from ..data import markets_data
from ..models import CurrencyCode, MarketSymbol, FetchMarketResponse, Market


async def fetch_market(self, symbol: Union[MarketSymbol, str]) -> Optional[FetchMarketResponse]:
    symbol = MarketSymbol.from_string(symbol) if isinstance(symbol, str) else symbol

    if self.markets != None and symbol in self.markets:
        return self.markets[symbol]

    market_data = (
        markets_data[self.params.network][str(symbol)]
        if self.params.network != None and self.params.network in markets_data
        else None
    )

    if market_data != None:
        for network in markets_data:
            markets = markets_data[network]
            if str(symbol) in markets:
                market_data = markets[str(symbol)]
                break

    if market_data == None:
        return

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

    return Market.from_dict(market)
