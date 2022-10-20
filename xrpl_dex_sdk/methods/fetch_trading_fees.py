from ..models.methods.fetch_trading_fees import FetchTradingFeesResponse
from ..models.ccxt.markets import Markets


async def fetch_trading_fees(self) -> FetchTradingFeesResponse:
    markets: Markets = await self.fetch_markets()

    if markets == None:
        return []

    trading_fees: FetchTradingFeesResponse = []

    for symbol in markets:
        trading_fee = await self.fetch_trading_fee(symbol)
        if trading_fee != None:
            trading_fees.append(trading_fee)

    return trading_fees
