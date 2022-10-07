from ..models.methods.fetch_trading_fees import FetchTradingFeesResponse


def fetch_trading_fees(self) -> FetchTradingFeesResponse:
    markets = self.fetch_markets()
    result: list = []
    for market in markets:
        result.append(self.fetch_trading_fees(market))
    return result
