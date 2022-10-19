from typing import Dict

from ..models import CurrencyCode, Issuer, Issuers
from .. import constants

IssuersData: Dict[str, Issuers] = {}

IssuersData[constants.TESTNET] = {
    "AktaryTech": Issuer(
        name="AktaryTech",
        trusted=True,
        website="https://aktarytech.com",
        addresses=["rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"],
        currencies=[CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B")],
        transfer_rate=0,
    ),
}

IssuersData[constants.MAINNET] = {
    "Sologenic": Issuer(
        name="Sologenic",
        trusted=True,
        website="https://sologenic.com",
        addresses=["rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz"],
        currencies=[
            CurrencyCode(
                "534F4C4F00000000000000000000000000000000",
                "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
            )
        ],
        transfer_rate=0,
    ),
    "Coreum": Issuer(
        name="Coreum",
        trusted=True,
        website="https://coreum.com",
        addresses=["rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D"],
        currencies=[
            CurrencyCode(
                "434F524500000000000000000000000000000000",
                "rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
            )
        ],
        transfer_rate=0,
    ),
    "Multichain": Issuer(
        name="Multichain",
        trusted=True,
        website="https://multichain.org",
        addresses=[
            "rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
            "rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
        ],
        currencies=[
            CurrencyCode(
                "5553445400000000000000000000000000000000",
                "rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
            ),
            CurrencyCode(
                "5553444300000000000000000000000000000000",
                "rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
            ),
        ],
        transfer_rate=0,
    ),
    "GateHub": Issuer(
        name="GateHub",
        trusted=True,
        website="https://gatehub.net",
        addresses=[
            "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "r3ttJ41YnMrKiLqGUXJpQE8urqyMGjC8vE",
            "rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL",
            "rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h",
            "rDAN8tzydyNfnNf2bfUQY6iR96UbpvNsze",
            "rcyS4CeCZVYvTiKcxj6Sx32ibKwcDHLds",
            "rcXY84C4g14iFp6taFXjjQGVeHqSCh9RX",
            "rckzVpTnKpP4TJ1puQe827bV3X4oYtdTP",
            "rctArjqVvTHihekzDeecKo6mkTYTUSBNc",
        ],
        currencies=[
            CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
            CurrencyCode("EUR", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
            CurrencyCode("QAU", "r3ttJ41YnMrKiLqGUXJpQE8urqyMGjC8vE"),
            CurrencyCode("BTC", "rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL"),
            CurrencyCode("ETH", "rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h"),
            CurrencyCode("ETC", "rDAN8tzydyNfnNf2bfUQY6iR96UbpvNsze"),
            CurrencyCode("BCH", "rcyS4CeCZVYvTiKcxj6Sx32ibKwcDHLds"),
            CurrencyCode("DSH", "rcXY84C4g14iFp6taFXjjQGVeHqSCh9RX"),
            CurrencyCode("REP", "rckzVpTnKpP4TJ1puQe827bV3X4oYtdTP"),
            CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc"),
        ],
        transfer_rate=0,
    ),
    "Bitstamp": Issuer(
        name="Bitstamp",
        trusted=True,
        website="https://bitstamp.net",
        addresses=[
            "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
            "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
            "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
            "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
            "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
            "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
            "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
        ],
        currencies=[
            CurrencyCode("USD", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
            CurrencyCode("EUR", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
            CurrencyCode("JPY", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
            CurrencyCode("GBP", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
            CurrencyCode("CHF", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
            CurrencyCode("AUD", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
            CurrencyCode("BTC", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        ],
        transfer_rate=0,
    ),
    "CasinoCoin": Issuer(
        name="CasinoCoin",
        trusted=True,
        website="https://casinocoin.org",
        addresses=["rCSCManTZ8ME9EoLrSHHYKW8PPwWMgkwr"],
        currencies=[CurrencyCode("CSC", "rCSCManTZ8ME9EoLrSHHYKW8PPwWMgkwr")],
        transfer_rate=0,
    ),
    "Kudos": Issuer(
        name="Kudos",
        trusted=True,
        website="https://bitstamp.net",
        addresses=["rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb"],
        currencies=[CurrencyCode("XTK", "rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb")],
        transfer_rate=0,
    ),
    "Allvor": Issuer(
        name="Allvor",
        trusted=True,
        website="https://bitstamp.net",
        addresses=["raEQc5krJ2rUXyi6fgmUAf63oAXmF7p6jp"],
        currencies=[CurrencyCode("ALV", "raEQc5krJ2rUXyi6fgmUAf63oAXmF7p6jp")],
        transfer_rate=0,
    ),
}
