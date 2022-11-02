from ..models import FetchTradingFeesResponse, Markets


async def fetch_trading_fees(self) -> FetchTradingFeesResponse:
    """Returns information about the fees incurred while trading on any market."""

    markets: Markets = await self.fetch_markets()

    if markets == None:
        return []

    trading_fees: FetchTradingFeesResponse = []

    for symbol in markets:
        trading_fee = await self.fetch_trading_fee(symbol)
        if trading_fee != None:
            trading_fees.append(trading_fee)

    return trading_fees
