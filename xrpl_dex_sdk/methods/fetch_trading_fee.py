from typing import Optional
from ..models import FetchTradingFeeResponse, MarketSymbol, Market, TradingFee


async def fetch_trading_fee(self, symbol: MarketSymbol) -> Optional[FetchTradingFeeResponse]:
    market: Market = await self.fetch_market(symbol)

    if market == None:
        return

    return TradingFee(
        symbol=symbol,
        base=market.base_fee if market.base_fee != None else 0,
        quote=market.quote_fee if market.quote_fee != None else 0,
        percentage=True,
        info={"market": market},
    )
