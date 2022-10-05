from enum import Enum
from typing import Any, Dict, NamedTuple, Optional

from .. import AccountAddress, MarketSymbol, UnixISOTimestamp, UnixTimestamp


class TradeId:
    def __init__(self, account: AccountAddress, sequence: int) -> None:
        self.account = account
        self.sequence = sequence
        self.id = account + ":" + str(sequence)

    def __repr__(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.id


class TradeType(Enum):
    Limit: str = "limit"


class TradeSide(Enum):
    Buy: str = "buy"
    Sell: str = "sell"


class TradeTakerOrMaker(Enum):
    Taker: str = ("taker",)
    Maker: str = ("maker",)


class Trade(NamedTuple):
    id: TradeId  # string trade id
    order: TradeId  # string order id or undefined/None/null
    datetime: UnixISOTimestamp  # ISO8601 datetime with milliseconds;
    timestamp: UnixTimestamp  # Unix timestamp in milliseconds
    symbol: MarketSymbol  # symbol in CCXT format
    type: Optional[TradeType]  # order type, 'market', 'limit', ... or undefined/None/null
    side: TradeSide  # direction of the trade, 'buy' or 'sell'
    amount: float  # amount of base currency
    price: float  # float price in quote currency
    takerOrMaker: TradeTakerOrMaker  # | 'maker'; string, 'taker' or 'maker'
    cost: float  # total cost (including fees), `price * amount`
    fee: Optional[float]
    info: Dict[str, Any]  # the original decoded JSON as is
