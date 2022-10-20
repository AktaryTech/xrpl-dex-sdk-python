from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional

from ..common import AccountAddress, MarketSymbol, UnixISOTimestamp, UnixTimestamp


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
    Taker: str = "taker"
    Maker: str = "maker"


class Trade(NamedTuple):
    # string trade id
    id: TradeId
    # string order id or undefined/None/null
    order: TradeId
    # ISO8601 datetime with milliseconds;
    datetime: UnixISOTimestamp
    # Unix timestamp in milliseconds
    timestamp: UnixTimestamp
    # symbol in CCXT format
    symbol: MarketSymbol
    # order type, 'market', 'limit', ... or undefined/None/null
    type: Optional[TradeType]
    # direction of the trade, 'buy' or 'sell'
    side: TradeSide
    # amount of base currency
    amount: float
    # float price in quote currency
    price: float
    # | 'maker'; string, 'taker' or 'maker'
    takerOrMaker: TradeTakerOrMaker
    # total cost (including fees), `price * amount`
    cost: float
    # transfer fees
    fee: Optional[float]
    # Raw response from exchange
    info: Dict[str, Any]


Trades = List[Trade]


__all__ = ["TradeId", "TradeType", "TradeSide", "TradeTakerOrMaker", "Trade", "Trades"]
