from ..models.methods.fetch_fees import FetchFeesResponse


async def fetch_fees(self) -> FetchFeesResponse:
    currencies = await self.fetch_currencies()
    transactions = await self.fetch_transaction_fees(
        currencies.keys() if currencies != None else {}
    )
    trading = await self.fetch_trading_fees()

    return {
        "transactions": transactions if transactions != None else [],
        "trading": trading if trading != None else [],
    }
