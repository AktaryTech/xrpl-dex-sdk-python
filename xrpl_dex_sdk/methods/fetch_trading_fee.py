from ..models.methods.fetch_trading_fee import FetchTradingFeeResponse
from ..models.common import MarketSymbol
from ..models.ccxt.markets import Market


async def fetch_trading_fee(self, symbol: MarketSymbol) -> FetchTradingFeeResponse:
    market: Market = await self.fetch_market(symbol)

    if market == None:
        return

    return {
        "symbol": symbol,
        "base": market["base_fee"] if "base_fee" in market else 0,
        "quote": market["quote_fee"] if "quote_fee" in market else 0,
        "percentage": True,
        "info": {"market": market},
    }
