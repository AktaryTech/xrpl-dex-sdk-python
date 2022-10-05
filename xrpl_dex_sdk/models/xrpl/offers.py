from enum import Enum


class OfferFlags(Enum):
    LSF_PASSIVE: int = 65536
    LSF_SELL: int = 131072


class OfferCreateFlags(Enum):
    TF_FILL_OR_KILL: int = 262144
    TF_IMMEDIATE_OR_CANCEL: int = 131072
    TF_PASSIVE: int = 65536
    TF_SELL: int = 524288
