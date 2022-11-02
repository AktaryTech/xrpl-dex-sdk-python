from enum import Enum


class XrplErrorTypes(Enum):
    ENTRY_NOT_FOUND = "entryNotFound"
    NO_CLOSED_LEDGER = "noClosed"
    NO_CURRENT_LEDGER = "noCurrent"
    NO_NETWORK = "noNetwork"
    TOO_BUSY = "tooBusy"
    TXN_NOT_FOUND = "txnNotFound"


class XrplTransactionErrorTypes(Enum):
    NO_ISSUER = "tecNO_ISSUER"
    UNFUNDED_OFFER = "tecUNFUNDED_OFFER"
