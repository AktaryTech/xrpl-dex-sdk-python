from typing import Any, Dict, cast

from xrpl_dex_sdk.models import (
    Currency,
    Order,
    OrderId,
    OrderSide,
    OrderTimeInForce,
    OrderType,
    OrderStatus,
    CurrencyCode,
    MarketSymbol,
    OrderBook,
    Trade,
    OrderBooks,
    OrderBookLevel,
    TradeId,
    TradeType,
    TradeSide,
    TradeTakerOrMaker,
)


fetch_order_book_response: OrderBooks = {}


fetch_order_book_response[
    MarketSymbol(
        CurrencyCode.from_string("AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"),
        CurrencyCode("XRP"),
    )
] = OrderBook.from_dict(
    {
        "symbol": MarketSymbol(
            CurrencyCode.from_string("AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"),
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

fetch_currencies_response = {
    CurrencyCode(
        currency="534F4C4F00000000000000000000000000000000",
        issuer="rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
    ): Currency(
        code=CurrencyCode(
            currency="534F4C4F00000000000000000000000000000000",
            issuer="rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        ),
        fee=0.0001,
        name="SOLO",
        issuer_name="Sologenic",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/94/e0ac1db308c4c90bc2e4fef8d79c204400714b8cbc6e75cc99177af9862fb637.png",
        precision=None,
    ),
    CurrencyCode(
        currency="434F524500000000000000000000000000000000",
        issuer="rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
    ): Currency(
        code=CurrencyCode(
            currency="434F524500000000000000000000000000000000",
            issuer="rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
        ),
        fee=None,
        name="CORE",
        issuer_name="Coreum",
        logo="https://docs.sologenic.com/dex/assets/mainnet/core-logo.png",
        precision=None,
    ),
    CurrencyCode(
        currency="5553445400000000000000000000000000000000",
        issuer="rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
    ): Currency(
        code=CurrencyCode(
            currency="5553445400000000000000000000000000000000",
            issuer="rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
        ),
        fee=None,
        name="USDT",
        issuer_name="Multichain",
        logo="https://storage.googleapis.com/sg-dex-production-331211-public-uploads/USDT.png",
        precision=None,
    ),
    CurrencyCode(
        currency="5553444300000000000000000000000000000000",
        issuer="rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
    ): Currency(
        code=CurrencyCode(
            currency="5553444300000000000000000000000000000000",
            issuer="rDsvn6aJG4YMQdHnuJtP9NLrFp18JYTJUf",
        ),
        fee=None,
        name="USDC",
        issuer_name="Multichain",
        logo="https://storage.googleapis.com/sg-dex-production-331211-public-uploads/USDC.png",
        precision=None,
    ),
    CurrencyCode(currency="USD", issuer="rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"): Currency(
        code=CurrencyCode(currency="USD", issuer="rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
        fee=0.002,
        name="USD",
        issuer_name="GateHub",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/90/d1a6c64dd038e8b5325442fa4471d9485a3d9052d0908c4630bf9b557d1de920.png",
        precision=None,
    ),
    CurrencyCode(currency="USD", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode(currency="USD", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        fee=0.002,
        name="USD",
        issuer_name="Bitstamp",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/79/d1a6c64dd038e8b5325442fa4471d9485a3d9052d0908c4630bf9b557d1de920.png",
        precision=None,
    ),
    CurrencyCode(currency="EUR", issuer="rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"): Currency(
        code=CurrencyCode(currency="EUR", issuer="rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
        fee=0.002,
        name="EUR",
        issuer_name="GateHub",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/91/2a7b19867db37f479185edd8fcad63ead88053beea4032e0a78453b79c08b7a5.png",
        precision=None,
    ),
    CurrencyCode(currency="EUR", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode(currency="EUR", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        fee=0.002,
        name="EUR",
        issuer_name="Bitstamp",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/80/2a7b19867db37f479185edd8fcad63ead88053beea4032e0a78453b79c08b7a5.png",
        precision=None,
    ),
    CurrencyCode(currency="QAU", issuer="r3ttJ41YnMrKiLqGUXJpQE8urqyMGjC8vE"): Currency(
        code=CurrencyCode(currency="QAU", issuer="r3ttJ41YnMrKiLqGUXJpQE8urqyMGjC8vE"),
        fee=0.0025,
        name="QAU",
        issuer_name="GateHub",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/85/dc0988f396f8d6f62ce809a90c3473c89c489158e6fc0fbcc6eec7a40027791a.png",
        precision=None,
    ),
    CurrencyCode(currency="BTC", issuer="rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL"): Currency(
        code=CurrencyCode(currency="BTC", issuer="rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL"),
        fee=0.002,
        name="Bitcoin",
        issuer_name="GateHub",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/88/538f358995fadbb8b124f486170cfcd478b5e13e0e64fefc581899f80c526041.png",
        precision=None,
    ),
    CurrencyCode(currency="BTC", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode(currency="BTC", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        fee=0.002,
        name="BTC",
        issuer_name="Bitstamp",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/78/538f358995fadbb8b124f486170cfcd478b5e13e0e64fefc581899f80c526041.png",
        precision=None,
    ),
    CurrencyCode(currency="ETH", issuer="rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h"): Currency(
        code=CurrencyCode(currency="ETH", issuer="rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h"),
        fee=0.003,
        name="Ethereum",
        issuer_name="GateHub",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/89/12196fe3f52068fca470c064d11a6002ab77c05b5dfc55f3fca3990f90c66e5b.png",
        precision=None,
    ),
    CurrencyCode(currency="ETC", issuer="rDAN8tzydyNfnNf2bfUQY6iR96UbpvNsze"): Currency(
        code=CurrencyCode(currency="ETC", issuer="rDAN8tzydyNfnNf2bfUQY6iR96UbpvNsze"),
        fee=0.003,
        name="Ethereum Classic",
        issuer_name="GateHub",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/84/e7c3c0ec6a920b0e183e3ef21d1333aec54a8f4ef768e4ca3f7b6743e6c2113d.png",
        precision=None,
    ),
    CurrencyCode(currency="BCH", issuer="rcyS4CeCZVYvTiKcxj6Sx32ibKwcDHLds"): Currency(
        code=CurrencyCode(currency="BCH", issuer="rcyS4CeCZVYvTiKcxj6Sx32ibKwcDHLds"),
        fee=0.003,
        name="Bitcoin Cash",
        issuer_name="GateHub",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/87/3235f479b84fa63dff05c7018a69f213008d9a2d3286227f400b73e09bc78b6f.png",
        precision=None,
    ),
    CurrencyCode(currency="DSH", issuer="rcXY84C4g14iFp6taFXjjQGVeHqSCh9RX"): Currency(
        code=CurrencyCode(currency="DSH", issuer="rcXY84C4g14iFp6taFXjjQGVeHqSCh9RX"),
        fee=0.003,
        name="DASH",
        issuer_name="GateHub",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/83/41baaee2809661b8e8431f3fb0b23bbfb0d0af7773c912836da94583c65ccb53.png",
        precision=None,
    ),
    CurrencyCode(currency="REP", issuer="rckzVpTnKpP4TJ1puQe827bV3X4oYtdTP"): Currency(
        code=CurrencyCode(currency="REP", issuer="rckzVpTnKpP4TJ1puQe827bV3X4oYtdTP"),
        fee=0.003,
        name="Augur",
        issuer_name="GateHub",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/86/4a5879cf2b054eb6e73a12597133cfd5c072e933514c439a9ddff3013c3fa620.png",
        precision=None,
    ),
    CurrencyCode(currency="SGB", issuer="rctArjqVvTHihekzDeecKo6mkTYTUSBNc"): Currency(
        code=CurrencyCode(currency="SGB", issuer="rctArjqVvTHihekzDeecKo6mkTYTUSBNc"),
        fee=0.003,
        name="Songbird",
        issuer_name="GateHub",
        logo=None,
        precision=None,
    ),
    CurrencyCode(currency="JPY", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode(currency="JPY", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        fee=0.002,
        name="JPY",
        issuer_name="Bitstamp",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/82/30757613c39ece8e5fa127a6094a9192cfef4f6043ee3a99b8a8615c4132f666.png",
        precision=None,
    ),
    CurrencyCode(currency="GBP", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode(currency="GBP", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        fee=0.002,
        name="GBP",
        issuer_name="Bitstamp",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/81/ea2a9011fa0d4fc184b40a9ac4ce463ae506b7e058253bf7d351d142f4e45af9.png",
        precision=None,
    ),
    CurrencyCode(currency="CHF", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode(currency="CHF", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        fee=0.002,
        name="CHF",
        issuer_name="Bitstamp",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/76/07740c2f86c82895ca47eaf77fe231ee3ffeaf737c5b04630e53d51040aa4010.png",
        precision=None,
    ),
    CurrencyCode(currency="AUD", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"): Currency(
        code=CurrencyCode(currency="AUD", issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
        fee=0.002,
        name="AUD",
        issuer_name="Bitstamp",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/77/817070a3a714a98315fce9b9e3a734b413867adc4ac4f6302469419e89982218.png",
        precision=None,
    ),
    CurrencyCode(currency="CSC", issuer="rCSCManTZ8ME9EoLrSHHYKW8PPwWMgkwr"): Currency(
        code=CurrencyCode(currency="CSC", issuer="rCSCManTZ8ME9EoLrSHHYKW8PPwWMgkwr"),
        fee=None,
        name="CSC",
        issuer_name="CasinoCoin",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/92/ce0cfa95bb8744b76a56e430280a614aa2f12b160b39b54d85b8dbf336c97891.png",
        precision=None,
    ),
    CurrencyCode(currency="XTK", issuer="rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb"): Currency(
        code=CurrencyCode(currency="XTK", issuer="rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb"),
        fee=None,
        name="XTK",
        issuer_name="Kudos",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/75/9e9ba69bc5ec358069714e2a40d540da37db9b3c15490656cea9f54871b51068.png",
        precision=None,
    ),
    CurrencyCode(currency="ALV", issuer="raEQc5krJ2rUXyi6fgmUAf63oAXmF7p6jp"): Currency(
        code=CurrencyCode(currency="ALV", issuer="raEQc5krJ2rUXyi6fgmUAf63oAXmF7p6jp"),
        fee=None,
        name="ALV",
        issuer_name="Allvor",
        logo="https://storage.googleapis.com/cfex-prod-uploads/uploads/93/8157b25078956f85756f7228effa0886035ae9669d47ac45afb275b9574cc516.png",
        precision=None,
    ),
}

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


fetch_order_responses: Dict[OrderId, Order] = {}

fetch_order_responses[
    OrderId.from_string("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z:31617670")
] = Order.from_dict(
    {
        "id": OrderId.from_string("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z:31617670"),
        "client_order_id": "29B699A1C221904E43650999C5BA5C3B32E6416E4CA390E64EF4392FFACF4406",
        "datetime": "2022-09-30T19:55:51.000Z",
        "timestamp": 1664567751000,
        "last_trade_timestamp": 1664568213000,
        "status": OrderStatus.Closed,
        "symbol": MarketSymbol.from_string("AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP"),
        "type": OrderType.Limit,
        "time_in_force": OrderTimeInForce.GoodTillCanceled,
        "side": OrderSide.Sell,
        "amount": 8.0,
        "price": 1.5,
        "average": 0.666666666666667,
        "filled": 7.5,
        "remaining": 0.5,
        "cost": 5.0,
        "trades": [
            Trade.from_dict(
                {
                    "id": TradeId.from_string("rLg33RykRFBxoJsTknkE5ekmoVDPmAPJwU:31617724"),
                    "order": OrderId.from_string("r3xYuG3dNF4oHBLXwEdFmFKGm9TWzqGT7z:31617670"),
                    "datetime": "2022-09-30T20:03:33.000Z",
                    "timestamp": 1664568213000,
                    "symbol": MarketSymbol.from_string(
                        "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
                    ),
                    "type": TradeType.Limit,
                    "side": TradeSide.Buy,
                    "amount": 7.5,
                    "price": 0.666666666666667,
                    "taker_or_maker": TradeTakerOrMaker.Taker,
                    "cost": 5.0,
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
                        "currency": CurrencyCode.from_string(
                            "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"
                        ),
                        "cost": 0.025,
                        "rate": 0.005,
                        "percentage": True,
                    },
                }
            )
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
)

fetch_trades_expected_responses: Dict[str, Dict[str, Any]] = {
    "by_trade_id": {},
    "by_order_id": {},
    "by_symbol": {},
}

_trade_1 = {
    "id": "r3KC7iM1GPLmvg1MVTXbXmoC87yyyuFRf2:67956678",
    "order": "rpXhhWmCvDwkzNtRbm7mmD1vZqdfatQNEe:59349452",
    "datetime": "2022-10-21T02:19:30.000Z",
    "timestamp": 1666318770000,
    "symbol": "XRP/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
    "type": "limit",
    "side": "sell",
    "amount": 5254.779017,
    "price": 0.4462306799635816,
    "taker_or_maker": "maker",
    "cost": 2344.843613814271,
}

fetch_trades_expected_responses["by_trade_id"][_trade_1["id"]] = _trade_1
fetch_trades_expected_responses["by_order_id"][_trade_1["order"]] = _trade_1
fetch_trades_expected_responses["by_symbol"][_trade_1["symbol"]] = _trade_1
