from typing import Any, Dict

from xrpl_dex_sdk.data import CurrenciesData
from xrpl_dex_sdk import constants
from xrpl_dex_sdk.models import (
    Currencies,
    CurrencyCode,
    MarketSymbol,
    OrderBook,
    OrderBooks,
    OrderBookLevel,
)


fetch_order_book_response: OrderBooks = {}


fetch_order_book_response[
    MarketSymbol(
        CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"), CurrencyCode("XRP")
    )
] = OrderBook.from_dict(
    {
        "symbol": MarketSymbol(
            CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"),
            CurrencyCode("XRP"),
        ),
        "nonce": 30419081,
        "bids": [],
        "asks": [[0.5, 19.5], [0.5, 50.0], [0.5, 50.0]],
        "level": OrderBookLevel.L2,
        "timestamp": None,
        "datetime": None,
    }
)

fetch_currencies_response: Currencies = CurrenciesData[constants.MAINNET]
# fetch_currencies_response: Currencies = {
#     "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz": {
#         "code": "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
#         "name": "SOLO",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/94/e0ac1db308c4c90bc2e4fef8d79c204400714b8cbc6e75cc99177af9862fb637.png",
#         "issuer_name": "Sologenic",
#     },
#     "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D": {
#         "code": "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
#         "name": "CORE",
#         "logo": "https://docs.sologenic.com/dex/assets/mainnet/core-logo.png",
#         "issuer_name": "Coreum",
#     },
#     "5553445400000000000000000000000000000000+rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf": {
#         "code": "5553445400000000000000000000000000000000+rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
#         "name": "USDT",
#         "logo": "https://storage.googleapis.com/sg-dex-production-331211-public-uploads/USDT.png",
#         "issuer_name": "Multichain",
#     },
#     "5553444300000000000000000000000000000000+rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf": {
#         "code": "5553444300000000000000000000000000000000+rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
#         "name": "USDC",
#         "logo": "https://storage.googleapis.com/sg-dex-production-331211-public-uploads/USDC.png",
#         "issuer_name": "Multichain",
#     },
#     "USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq": {
#         "code": "USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
#         "name": "USD",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/90/d1a6c64dd038e8b5325442fa4471d9485a3d9052d0908c4630bf9b557d1de920.png",
#         "issuer_name": "GateHub",
#     },
#     "USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B": {
#         "code": "USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#         "name": "USD",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/79/d1a6c64dd038e8b5325442fa4471d9485a3d9052d0908c4630bf9b557d1de920.png",
#         "issuer_name": "Bitstamp",
#     },
#     "EUR+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq": {
#         "code": "EUR+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
#         "name": "EUR",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/91/2a7b19867db37f479185edd8fcad63ead88053beea4032e0a78453b79c08b7a5.png",
#         "issuer_name": "GateHub",
#     },
#     "EUR+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B": {
#         "code": "EUR+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#         "name": "EUR",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/80/2a7b19867db37f479185edd8fcad63ead88053beea4032e0a78453b79c08b7a5.png",
#         "issuer_name": "Bitstamp",
#     },
#     "QAU+r3ttJ41YnMrKiLqGUXJpQE8urqyMGjC8vE": {
#         "code": "QAU+r3ttJ41YnMrKiLqGUXJpQE8urqyMGjC8vE",
#         "name": "QAU",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/85/dc0988f396f8d6f62ce809a90c3473c89c489158e6fc0fbcc6eec7a40027791a.png",
#         "issuer_name": "GateHub",
#     },
#     "BTC+rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL": {
#         "code": "BTC+rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL",
#         "name": "Bitcoin",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/88/538f358995fadbb8b124f486170cfcd478b5e13e0e64fefc581899f80c526041.png",
#         "issuer_name": "GateHub",
#     },
#     "BTC+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B": {
#         "code": "BTC+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#         "name": "BTC",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/78/538f358995fadbb8b124f486170cfcd478b5e13e0e64fefc581899f80c526041.png",
#         "issuer_name": "Bitstamp",
#     },
#     "ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h": {
#         "code": "ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h",
#         "name": "Ethereum",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/89/12196fe3f52068fca470c064d11a6002ab77c05b5dfc55f3fca3990f90c66e5b.png",
#         "issuer_name": "GateHub",
#     },
#     "ETC+rDAN8tzydyNfnNf2bfUQY6iR96UbpvNsze": {
#         "code": "ETC+rDAN8tzydyNfnNf2bfUQY6iR96UbpvNsze",
#         "name": "Ethereum Classic",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/84/e7c3c0ec6a920b0e183e3ef21d1333aec54a8f4ef768e4ca3f7b6743e6c2113d.png",
#         "issuer_name": "GateHub",
#     },
#     "BCH+rcyS4CeCZVYvTiKcxj6Sx32ibKwcDHLds": {
#         "code": "BCH+rcyS4CeCZVYvTiKcxj6Sx32ibKwcDHLds",
#         "name": "Bitcoin Cash",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/87/3235f479b84fa63dff05c7018a69f213008d9a2d3286227f400b73e09bc78b6f.png",
#         "issuer_name": "GateHub",
#     },
#     "DSH+rcXY84C4g14iFp6taFXjjQGVeHqSCh9RX": {
#         "code": "DSH+rcXY84C4g14iFp6taFXjjQGVeHqSCh9RX",
#         "name": "DASH",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/83/41baaee2809661b8e8431f3fb0b23bbfb0d0af7773c912836da94583c65ccb53.png",
#         "issuer_name": "GateHub",
#     },
#     "REP+rckzVpTnKpP4TJ1puQe827bV3X4oYtdTP": {
#         "code": "REP+rckzVpTnKpP4TJ1puQe827bV3X4oYtdTP",
#         "name": "Augur",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/86/4a5879cf2b054eb6e73a12597133cfd5c072e933514c439a9ddff3013c3fa620.png",
#         "issuer_name": "GateHub",
#     },
#     "SGB+rctArjqVvTHihekzDeecKo6mkTYTUSBNc": {
#         "code": "SGB+rctArjqVvTHihekzDeecKo6mkTYTUSBNc",
#         "name": "Songbird",
#         "issuer_name": "GateHub",
#     },
#     "JPY+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B": {
#         "code": "JPY+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#         "name": "JPY",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/82/30757613c39ece8e5fa127a6094a9192cfef4f6043ee3a99b8a8615c4132f666.png",
#         "issuer_name": "Bitstamp",
#     },
#     "GBP+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B": {
#         "code": "GBP+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#         "name": "GBP",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/81/ea2a9011fa0d4fc184b40a9ac4ce463ae506b7e058253bf7d351d142f4e45af9.png",
#         "issuer_name": "Bitstamp",
#     },
#     "CHF+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B": {
#         "code": "CHF+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#         "name": "CHF",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/76/07740c2f86c82895ca47eaf77fe231ee3ffeaf737c5b04630e53d51040aa4010.png",
#         "issuer_name": "Bitstamp",
#     },
#     "AUD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B": {
#         "code": "AUD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
#         "name": "AUD",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/77/817070a3a714a98315fce9b9e3a734b413867adc4ac4f6302469419e89982218.png",
#         "issuer_name": "Bitstamp",
#     },
#     "CSC+rCSCManTZ8ME9EoLrSHHYKW8PPwWMgkwr": {
#         "code": "CSC+rCSCManTZ8ME9EoLrSHHYKW8PPwWMgkwr",
#         "name": "CSC",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/92/ce0cfa95bb8744b76a56e430280a614aa2f12b160b39b54d85b8dbf336c97891.png",
#         "issuer_name": "CasinoCoin",
#     },
#     "XTK+rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb": {
#         "code": "XTK+rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb",
#         "name": "XTK",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/75/9e9ba69bc5ec358069714e2a40d540da37db9b3c15490656cea9f54871b51068.png",
#         "issuer_name": "Kudos",
#     },
#     "ALV+raEQc5krJ2rUXyi6fgmUAf63oAXmF7p6jp": {
#         "code": "ALV+raEQc5krJ2rUXyi6fgmUAf63oAXmF7p6jp",
#         "name": "ALV",
#         "logo": "https://storage.googleapis.com/cfex-prod-uploads/uploads/93/8157b25078956f85756f7228effa0886035ae9669d47ac45afb275b9574cc516.png",
#         "issuer_name": "Allvor",
#     },
# }

create_order_responses: Dict[str, Any] = {}

create_order_responses["rpkeJcxB2y5BeAFyycuWwdTTcR3og2a3SR:30419079"] = {
    "Account": "rpkeJcxB2y5BeAFyycuWwdTTcR3og2a3SR",
    "Fee": "10",
    "Flags": 524288,
    "LastLedgerSequence": 31813272,
    "Sequence": 30419079,
    "SigningPubKey": "02155F290580BC63BD445368B7B2101C0A8997FA0E18D591C181AC4C6342499AF3",
    "TakerGets": "50000000",
    "TakerPays": {
        "currency": "AKT",
        "issuer": "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
        "value": "25",
    },
    "TransactionType": "OfferCreate",
    "TxnSignature": "30440220478EEC4A1096AA045E75C9FAF2196C9F594AE61DF57E18A305F445E5AF868D60022026C8FBC9AE39777A0616119930EEDC65A6046A1D201BB0343453C83735BFF77B",
    "hash": "28E3B19CF04CEDB3403D3187054F992BA6453CA9177E7C32ECAE23AF56382B6F",
}


fetch_order_responses: Dict[str, Any] = {}

fetch_order_responses["r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z:31617670"] = {
    "id": "r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z:31617670",
    "clientOrderId": "29B699A1C221904E43650999C5BA5C3B32E6416E4CA390E64EF4392FFACF4406",
    "datetime": "2022-09-30T19:55:51.000Z",
    "timestamp": 1664567751000,
    "lastTradeTimestamp": 1664568213000,
    "status": "closed",
    "symbol": "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP",
    "type": "limit",
    "timeInForce": "GTC",
    "side": "sell",
    "amount": "8",
    "price": "1.5",
    "average": "0.666666666666667",
    "filled": "7.5",
    "remaining": "0.5",
    "cost": "5",
    "trades": [
        {
            "id": "rLg33RykRFBxoJsTknkE5ekmoVDPmAPJwU:31617724",
            "order": "r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z:31617670",
            "datetime": "2022-09-30T20:03:33.000Z",
            "timestamp": 1664568213000,
            "symbol": "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
            "type": "limit",
            "side": "buy",
            "amount": "7.5",
            "price": "0.666666666666667",
            "takerOrMaker": "taker",
            "cost": "5",
            "info": {
                "transaction": {
                    "Account": "rLg33RykRFBxoJsTknkE5ekmoVDPmAPJwU",
                    "BookDirectory": "",
                    "BookNode": "0",
                    "LedgerEntryType": "Offer",
                    "Flags": 0,
                    "OwnerNode": "0",
                    "Sequence": 31617724,
                    "TakerGets": {
                        "currency": "AKT",
                        "issuer": "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
                        "value": "5",
                    },
                    "TakerPays": "7500000",
                    "index": "859D3BA7545DD846325DA52114D7EFA43103BC279F048CD3CD8EA812989D6AC5",
                    "PreviousTxnID": "39F5F7B36AE1F7D226AAEA8807D830363948AA1D919188D77C709FDF0A3DE16E",
                    "PreviousTxnLgrSeq": 0,
                }
            },
            "fee": {
                "currency": "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
                "cost": "0.025",
                "rate": "0.005",
                "percentage": True,
            },
        }
    ],
    "info": {
        "transactionData": {
            "transaction": {
                "Account": "r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z",
                "Fee": "12",
                "Flags": 524288,
                "LastLedgerSequence": 31618763,
                "Sequence": 31617670,
                "SigningPubKey": "ED8B9B26AE09C875052726030E10AFDD27DDCFA89BBFB57237A3AC1FE72F0911F1",
                "TakerGets": {
                    "currency": "AKT",
                    "issuer": "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
                    "value": "8",
                },
                "TakerPays": "12000000",
                "TransactionType": "OfferCreate",
                "TxnSignature": "6CD1B07EB1980A35C26F6A9E173FC7C7E0686DB732074F213DB2B353458868A9A6A659E8C877BE155DE4E52E2089156909083C315D2951F742575B0CEC1B7001",
                "date": 717882951,
                "hash": "39F5F7B36AE1F7D226AAEA8807D830363948AA1D919188D77C709FDF0A3DE16E",
                "inLedger": 31618745,
                "ledger_index": 31618745,
                "validated": True,
            },
            "metadata": {
                "AffectedNodes": [],
                "TransactionIndex": 2,
                "TransactionResult": "tesSUCCESS",
            },
            "offers": [],
            "date": 717882951,
        }
    },
}
