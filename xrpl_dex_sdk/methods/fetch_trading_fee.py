import json
from ..models.methods.fetch_trading_fee import FetchTradingFeeResponse


def fetch_trading_fee(self, symbol: str) -> FetchTradingFeeResponse:
    markets = self.fetch_markets()
    if symbol in markets is False:
        raise Exception("No symbol in markets data")

    market_symbol = markets.get(symbol)
    base_fee = market_symbol.get("baseFee", 0)
    base_issuer = market_symbol.get("baseIssuer")
    quote_fee = market_symbol.get("quoteFee", 0)
    quote_issuer = market_symbol.get("quoteIssuer")
    response = {
        "symbol": symbol,
        "base": base_fee,
        "quote": quote_fee,
        "percentage": True,
        "info": json.dumps({"market": market_symbol}),
    }
    if base_issuer:
        response["baseIssuer"] = base_issuer
    if quote_issuer:
        response["quoteIssuer"] = quote_issuer

    return response
