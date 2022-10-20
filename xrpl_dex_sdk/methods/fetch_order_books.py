from typing import List

from ..constants import DEFAULT_LIMIT
from ..models import (
    FetchOrderBooksParams,
    FetchOrderBooksResponse,
    MarketSymbol,
)


async def fetch_order_books(
    self,
    symbols: List[MarketSymbol],
    limit: int = DEFAULT_LIMIT,
    params: FetchOrderBooksParams = FetchOrderBooksParams(),
) -> FetchOrderBooksResponse:
    order_books: FetchOrderBooksResponse = {}

    for symbol in symbols:
        order_book = await self.fetch_order_book(
            symbol=symbol,
            limit=limit,
            params=params.symbols[symbol] if params.symbols != None else None,
        )
        if order_book != None:
            order_books[symbol] = order_book

    return order_books
