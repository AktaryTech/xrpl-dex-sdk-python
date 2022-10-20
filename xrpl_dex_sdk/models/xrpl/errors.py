from enum import Enum


class XrplErrorTypes(Enum):
    ENTRY_NOT_FOUND: str = "entryNotFound"
    NO_CLOSED_LEDGER: str = "noClosed"
    NO_CURRENT_LEDGER: str = "noCurrent"
    NO_NETWORK: str = "noNetwork"
    TOO_BUSY: str = "tooBusy"
    TXN_NOT_FOUND: str = "txnNotFound"


class XrplTransactionErrorTypes(Enum):
    NO_ISSUER: str = "tecNO_ISSUER"
    UNFUNDED_OFFER: str = "tecUNFUNDED_OFFER"


__all__ = ["XrplErrorTypes", "XrplTransactionErrorTypes"]
