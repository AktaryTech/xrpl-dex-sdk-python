from enum import Enum
from hashlib import sha512
import base58

from xrpl.utils import str_to_hex
from xrpl.core.addresscodec import codec

#
# XRP Ledger namespace prefixes.
#
# The XRP Ledger is a key-value store. In order to avoid name collisions
# names are partitioned into namespaces.
#
# Each namespace is just a single character prefix.
#
# See [LedgerNameSpace enum](https://github.com/ripple/rippled/blob/master/src/ripple/protocol/LedgerFormats.h#L100).
#
class LedgerNameSpaces(Enum):
    account: str = "a"
    dirNode: str = "d"
    generatorMap: str = "g"
    rippleState: str = "r"
    offer: str = "o"
    ownerDir: str = "O"
    bookDir: str = "B"
    contract: str = "c"
    skipList: str = "s"
    escrow: str = "u"
    amendment: str = "f"
    feeSettings: str = "e"
    ticket: str = "T"
    signerList: str = "S"
    paychan: str = "x"
    check: str = "C"
    depositPreauth: str = "p"


def sha_512_half(hex: str) -> str:
    return sha512(bytes.fromhex(hex)).digest().hex().upper()[:64]


def hash_offer_id(address: str, sequence: int) -> str:
    hex_prefix = LedgerNameSpaces.offer.value.encode("utf-8").hex()
    prefix_pad_size = 2 - len(hex_prefix)
    if prefix_pad_size > 0:
        for _ in range(prefix_pad_size):
            hex_prefix = "0" + hex_prefix
    prefix = "00" + hex_prefix

    hex_sequence = hex(sequence).split("0x")[1]
    sequence_pad_size = 8 - len(hex_sequence)
    if sequence_pad_size > 0:
        for _ in range(sequence_pad_size):
            hex_sequence = "0" + hex_sequence

    base58_address = base58.b58decode_check(
        address,
        alphabet="rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz".encode("utf-8"),
    )[1:]

    offer_id_hash = sha_512_half((prefix + base58_address.hex() + hex_sequence))

    return offer_id_hash
