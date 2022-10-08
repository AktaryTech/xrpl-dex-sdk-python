from ..models.methods.fetch_fees import FetchFeesResponse


def fetch_fees(self) -> FetchFeesResponse:
    currencies = self.fetch_currencies()
    transactions = self.fetch_transaction_fees(
        currencies.keys() if currencies != None else currencies.keys()
    )
    trading = self.fetch_trading_fees()

    return {"transactions": transactions, "trading": trading}
