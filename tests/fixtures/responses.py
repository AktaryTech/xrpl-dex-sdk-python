from typing import Any, Dict

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
    "status": "open",
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
