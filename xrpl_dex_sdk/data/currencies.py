from typing import Dict

from ..models import CurrencyCode, Currency, Currencies
from .. import constants


CurrenciesData: Dict[str, Currencies] = {}

CurrenciesData[constants.TESTNET] = {
    CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"): Currency(
        code=CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"),
        name="AKT",
        issuer_name="AktaryTech",
    ),
}


CurrenciesData[constants.MAINNET] = {
    CurrencyCode(
        "534F4C4F00000000000000000000000000000000",
        "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
    ): Currency(
        code=CurrencyCode(
            "534F4C4F00000000000000000000000000000000",
            "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        ),
        name="SOLO",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/94/e0ac1db308c4c90bc2e4fef8d79c204400714b8cbc6e75cc99177af9862fb637.png",
        issuer_name="Sologenic",
    ),
    CurrencyCode(
        "434F524500000000000000000000000000000000",
        "rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
    ): Currency(
        code=CurrencyCode(
            "434F524500000000000000000000000000000000",
            "rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
        ),
        name="CORE",
        logo="https://docs.sologenic.com/dex/assets/mainnet/core-logo.png",
        issuer_name="Coreum",
    ),
    CurrencyCode(
        "5553445400000000000000000000000000000000",
        "rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
    ): Currency(
        code=CurrencyCode(
            "5553445400000000000000000000000000000000",
            "rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
        ),
        name="USDT",
        logo="https://storage.googleapis.com/sg-dex-production-331211-public-uploads/USDT.png",
        issuer_name="Multichain",
    ),
    CurrencyCode(
        "5553444300000000000000000000000000000000",
        "rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
    ): Currency(
        code=CurrencyCode(
            "5553444300000000000000000000000000000000",
            "rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
        ),
        name="USDC",
        logo="https://storage.googleapis.com/sg-dex-production-331211-public-uploads/USDC.png",
        issuer_name="Multichain",
    ),
    CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"): Currency(
        code=CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
        name="USD",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/90/d1a6c64dd038e8b5325442fa4471d9485a3d9052d0908c4630bf9b557d1de920.png",
        issuer_name="GateHub",
    ),
    CurrencyCode("USD", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode("USD", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        name="USD",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/79/d1a6c64dd038e8b5325442fa4471d9485a3d9052d0908c4630bf9b557d1de920.png",
        issuer_name="Bitstamp",
    ),
    CurrencyCode("EUR", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"): Currency(
        code=CurrencyCode("EUR", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
        name="EUR",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/91/2a7b19867db37f479185edd8fcad63ead88053beea4032e0a78453b79c08b7a5.png",
        issuer_name="GateHub",
    ),
    CurrencyCode("EUR", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode("EUR", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        name="EUR",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/80/2a7b19867db37f479185edd8fcad63ead88053beea4032e0a78453b79c08b7a5.png",
        issuer_name="Bitstamp",
    ),
    CurrencyCode("QAU", "r3ttJ41YnMrKiLqGUXJpQE8urqyMGjC8vE"): Currency(
        code=CurrencyCode("QAU", "r3ttJ41YnMrKiLqGUXJpQE8urqyMGjC8vE"),
        name="QAU",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/85/dc0988f396f8d6f62ce809a90c3473c89c489158e6fc0fbcc6eec7a40027791a.png",
        issuer_name="GateHub",
    ),
    CurrencyCode("BTC", "rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL"): Currency(
        code=CurrencyCode("BTC", "rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL"),
        name="Bitcoin",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/88/538f358995fadbb8b124f486170cfcd478b5e13e0e64fefc581899f80c526041.png",
        issuer_name="GateHub",
    ),
    CurrencyCode("BTC", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode("BTC", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        name="BTC",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/78/538f358995fadbb8b124f486170cfcd478b5e13e0e64fefc581899f80c526041.png",
        issuer_name="Bitstamp",
    ),
    CurrencyCode("ETH", "rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h"): Currency(
        code=CurrencyCode("ETH", "rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h"),
        name="Ethereum",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/89/12196fe3f52068fca470c064d11a6002ab77c05b5dfc55f3fca3990f90c66e5b.png",
        issuer_name="GateHub",
    ),
    CurrencyCode("ETC", "rDAN8tzydyNfnNf2bfUQY6iR96UbpvNsze"): Currency(
        code=CurrencyCode("ETC", "rDAN8tzydyNfnNf2bfUQY6iR96UbpvNsze"),
        name="Ethereum Classic",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/84/e7c3c0ec6a920b0e183e3ef21d1333aec54a8f4ef768e4ca3f7b6743e6c2113d.png",
        issuer_name="GateHub",
    ),
    CurrencyCode("BCH", "rcyS4CeCZVYvTiKcxj6Sx32ibKwcDHLds"): Currency(
        code=CurrencyCode("BCH", "rcyS4CeCZVYvTiKcxj6Sx32ibKwcDHLds"),
        name="Bitcoin Cash",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/87/3235f479b84fa63dff05c7018a69f213008d9a2d3286227f400b73e09bc78b6f.png",
        issuer_name="GateHub",
    ),
    CurrencyCode("DSH", "rcXY84C4g14iFp6taFXjjQGVeHqSCh9RX"): Currency(
        code=CurrencyCode("DSH", "rcXY84C4g14iFp6taFXjjQGVeHqSCh9RX"),
        name="DASH",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/83/41baaee2809661b8e8431f3fb0b23bbfb0d0af7773c912836da94583c65ccb53.png",
        issuer_name="GateHub",
    ),
    CurrencyCode("REP", "rckzVpTnKpP4TJ1puQe827bV3X4oYtdTP"): Currency(
        code=CurrencyCode("REP", "rckzVpTnKpP4TJ1puQe827bV3X4oYtdTP"),
        name="Augur",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/86/4a5879cf2b054eb6e73a12597133cfd5c072e933514c439a9ddff3013c3fa620.png",
        issuer_name="GateHub",
    ),
    CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc"): Currency(
        code=CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc"),
        name="Songbird",
        issuer_name="GateHub",
    ),
    CurrencyCode("JPY", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode("JPY", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        name="JPY",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/82/30757613c39ece8e5fa127a6094a9192cfef4f6043ee3a99b8a8615c4132f666.png",
        issuer_name="Bitstamp",
    ),
    CurrencyCode("GBP", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode("GBP", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        name="GBP",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/81/ea2a9011fa0d4fc184b40a9ac4ce463ae506b7e058253bf7d351d142f4e45af9.png",
        issuer_name="Bitstamp",
    ),
    CurrencyCode("CHF", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode("CHF", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        name="CHF",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/76/07740c2f86c82895ca47eaf77fe231ee3ffeaf737c5b04630e53d51040aa4010.png",
        issuer_name="Bitstamp",
    ),
    CurrencyCode("AUD", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode("AUD", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        name="AUD",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/77/817070a3a714a98315fce9b9e3a734b413867adc4ac4f6302469419e89982218.png",
        issuer_name="Bitstamp",
    ),
    CurrencyCode("CSC", "rCSCManTZ8ME9EoLrSHHYKW8PPwWMgkwr"): Currency(
        code=CurrencyCode("CSC", "rCSCManTZ8ME9EoLrSHHYKW8PPwWMgkwr"),
        name="CSC",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/92/ce0cfa95bb8744b76a56e430280a614aa2f12b160b39b54d85b8dbf336c97891.png",
        issuer_name="CasinoCoin",
    ),
    CurrencyCode("XTK", "rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb"): Currency(
        code=CurrencyCode("XTK", "rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb"),
        name="XTK",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/75/9e9ba69bc5ec358069714e2a40d540da37db9b3c15490656cea9f54871b51068.png",
        issuer_name="Kudos",
    ),
    CurrencyCode("ALV", "raEQc5krJ2rUXyi6fgmUAf63oAXmF7p6jp"): Currency(
        code=CurrencyCode("ALV", "raEQc5krJ2rUXyi6fgmUAf63oAXmF7p6jp"),
        name="ALV",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/93/8157b25078956f85756f7228effa0886035ae9669d47ac45afb275b9574cc516.png",
        issuer_name="Allvor",
    ),
}
