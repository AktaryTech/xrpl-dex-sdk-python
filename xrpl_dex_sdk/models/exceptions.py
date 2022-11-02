class CCXTException(Exception):
    """Base Exception for CCXT."""

    pass


class BaseError(Exception):
    pass


#
# Exchange Errors
#
class ExchangeError(BaseError):
    pass


class AuthenticationError(ExchangeError):
    pass


class PermissionDenied(AuthenticationError):
    pass


class AccountNotEnabled(PermissionDenied):
    pass


class ArgumentsRequired(ExchangeError):
    pass


class BadRequest(ExchangeError):
    pass


class BadSymbol(BadRequest):
    pass


class BadOrderId(BadRequest):
    pass


class BadResponse(ExchangeError):
    pass


class InsufficientFunds(ExchangeError):
    pass


class InvalidAddress(ExchangeError):
    pass


class InvalidOrder(ExchangeError):
    pass


class OrderNotFound(InvalidOrder):
    pass


class CancelPending(InvalidOrder):
    pass


class NotSupported(ExchangeError):
    pass


class MarketNotFound(ExchangeError):
    pass


#
# Network Errors
#
class NetworkError(BaseError):
    pass


class DDoSProtection(NetworkError):
    pass


class RateLimitExceeded(DDoSProtection):
    pass


class ExchangeNotAvailable(NetworkError):
    pass


class RequestTimeout(NetworkError):
    pass
