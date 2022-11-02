from typing import Optional, Union
from ..data import MarketsData
from ..models import CurrencyCode, MarketSymbol, FetchMarketResponse, Market


async def fetch_market(self, symbol: Union[MarketSymbol, str]) -> Optional[FetchMarketResponse]:
    """
    Retrieves info about a single market being traded on the dEX.

    Parameters
    ----------
    symbol : xrpl_dex_sdk.models.MarketSymbol
        Market to get data for

    Returns
    -------
    xrpl_dex_sdk.models.FetchMarketResponse
        Market data
    """

    symbol = MarketSymbol.from_string(symbol) if isinstance(symbol, str) else symbol

    if self.markets != None and symbol in self.markets:
        return self.markets[symbol]

    market_data = (
        MarketsData[self.params.network][str(symbol)]
        if self.params.network != None and self.params.network in MarketsData
        else None
    )

    if market_data != None:
        for network in MarketsData:
            markets = MarketsData[network]
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
