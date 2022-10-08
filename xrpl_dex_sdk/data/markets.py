from typing import Dict

from ..models import Markets
from .. import constants

MarketsData: Dict[str, Markets] = {}

MarketsData[constants.TESTNET] = dict(
    {
        "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP": {
            "id": "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP",
            "symbol": "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP",
            "base": "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
            "quote": "XRP",
        },
        "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B": {
            "id": "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
            "symbol": "XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
            "base": "XRP",
            "quote": "AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
        },
    },
)

MarketsData[constants.MAINNET] = dict(
    {
        "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/XRP": {
            "id": "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/XRP",
            "symbol": "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/XRP",
            "base": "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
            "quote": "XRP",
        },
        "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D/XRP": {
            "id": "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D/XRP",
            "symbol": "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D/XRP",
            "base": "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
            "quote": "XRP",
        },
        "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D/534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz": {
            "id": "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D/534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
            "symbol": "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D/534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
            "base": "434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
            "quote": "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        },
        "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B": {
            "id": "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
            "symbol": "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
            "base": "534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
            "quote": "USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
        },
        "XRP/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq": {
            "id": "XRP/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "symbol": "XRP/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "base": "XRP",
            "quote": "USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
        },
        "XRP/EUR+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq": {
            "id": "XRP/EUR+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "symbol": "XRP/EUR+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "base": "XRP",
            "quote": "EUR+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
        },
        "XRP/SGB+rctArjqVvTHihekzDeecKo6mkTYTUSBNc": {
            "id": "XRP/SGB+rctArjqVvTHihekzDeecKo6mkTYTUSBNc",
            "symbol": "XRP/SGB+rctArjqVvTHihekzDeecKo6mkTYTUSBNc",
            "base": "XRP",
            "quote": "SGB+rctArjqVvTHihekzDeecKo6mkTYTUSBNc",
        },
        "XRP/ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h": {
            "id": "XRP/ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h",
            "symbol": "XRP/ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h",
            "base": "XRP",
            "quote": "ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h",
        },
        "XRP/XTK+rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb": {
            "id": "XRP/XTK+rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb",
            "symbol": "XRP/XTK+rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb",
            "base": "XRP",
            "quote": "XTK+rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb",
        },
        "XRP/5852646F67650000000000000000000000000000+rLqUC2eCPohYvJCEBJ77eCCqVL2uEiczjA": {
            "id": "XRP/5852646F67650000000000000000000000000000+rLqUC2eCPohYvJCEBJ77eCCqVL2uEiczjA",
            "symbol": "XRP/5852646F67650000000000000000000000000000+rLqUC2eCPohYvJCEBJ77eCCqVL2uEiczjA",
            "base": "XRP",
            "quote": "5852646F67650000000000000000000000000000+rLqUC2eCPohYvJCEBJ77eCCqVL2uEiczjA",
        },
        "XRP/58464C4F4B490000000000000000000000000000+rUtXeAXonpFpgKubAa7LxcLd7NFep92T1t": {
            "id": "XRP/58464C4F4B490000000000000000000000000000+rUtXeAXonpFpgKubAa7LxcLd7NFep92T1t",
            "symbol": "XRP/58464C4F4B490000000000000000000000000000+rUtXeAXonpFpgKubAa7LxcLd7NFep92T1t",
            "base": "XRP",
            "quote": "58464C4F4B490000000000000000000000000000+rUtXeAXonpFpgKubAa7LxcLd7NFep92T1t",
        },
        "XRP/4A554E4B00000000000000000000000000000000+r4pDJ7bT1rANe9nAdFR9pyVRwtJZQUEFpj": {
            "id": "XRP/4A554E4B00000000000000000000000000000000+r4pDJ7bT1rANe9nAdFR9pyVRwtJZQUEFpj",
            "symbol": "XRP/4A554E4B00000000000000000000000000000000+r4pDJ7bT1rANe9nAdFR9pyVRwtJZQUEFpj",
            "base": "XRP",
            "quote": "4A554E4B00000000000000000000000000000000+r4pDJ7bT1rANe9nAdFR9pyVRwtJZQUEFpj",
        },
        "XRP/5844554445000000000000000000000000000000+rU5LE7X6yyu9DuHsLdHhWSiUVTgpyRK1vz": {
            "id": "XRP/5844554445000000000000000000000000000000+rU5LE7X6yyu9DuHsLdHhWSiUVTgpyRK1vz",
            "symbol": "XRP/5844554445000000000000000000000000000000+rU5LE7X6yyu9DuHsLdHhWSiUVTgpyRK1vz",
            "base": "XRP",
            "quote": "5844554445000000000000000000000000000000+rU5LE7X6yyu9DuHsLdHhWSiUVTgpyRK1vz",
        },
        "XRP/457175696C69627269756D000000000000000000+rpakCr61Q92abPXJnVboKENmpKssWyHpwu": {
            "id": "XRP/457175696C69627269756D000000000000000000+rpakCr61Q92abPXJnVboKENmpKssWyHpwu",
            "symbol": "XRP/457175696C69627269756D000000000000000000+rpakCr61Q92abPXJnVboKENmpKssWyHpwu",
            "base": "XRP",
            "quote": "457175696C69627269756D000000000000000000+rpakCr61Q92abPXJnVboKENmpKssWyHpwu",
        },
        "XRP/ELS+rHXuEaRYnnJHbDeuBH5w8yPh5uwNVh5zAg": {
            "id": "XRP/ELS+rHXuEaRYnnJHbDeuBH5w8yPh5uwNVh5zAg",
            "symbol": "XRP/ELS+rHXuEaRYnnJHbDeuBH5w8yPh5uwNVh5zAg",
            "base": "XRP",
            "quote": "ELS+rHXuEaRYnnJHbDeuBH5w8yPh5uwNVh5zAg",
        },
        "BTC+rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq": {
            "id": "BTC+rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "symbol": "BTC+rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "base": "BTC+rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL",
            "quote": "USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
        },
        "ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq": {
            "id": "ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "symbol": "ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
            "base": "ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h",
            "quote": "USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
        },
    },
)
