from ..models.methods.fetch_markets import FetchMarketsResponse


def fetch_markets(self) -> FetchMarketsResponse:
    return self.load_data("markets.json")
