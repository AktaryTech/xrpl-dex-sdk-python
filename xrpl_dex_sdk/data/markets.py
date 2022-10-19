from typing import Dict

from ..models import Markets, MarketSymbol, CurrencyCode, Market
from .. import constants

MarketsData: Dict[str, Markets] = {}

MarketsData[constants.TESTNET] = {
    MarketSymbol(
        CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"), "XRP"
    ): Market(
        id="AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B/XRP",
        symbol=MarketSymbol(
            CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"), "XRP"
        ),
        base=CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"),
        quote=CurrencyCode("XRP"),
    ),
    MarketSymbol(
        "XRP", CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B")
    ): Market(
        id="XRP/AKT+rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B",
        symbol=MarketSymbol(
            "XRP", CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B")
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode("AKT", "rMZoAqwRn3BLbmFYL3exNVNVKrceYcNy6B"),
    ),
}


MarketsData[constants.MAINNET] = {
    MarketSymbol(
        CurrencyCode(
            "534F4C4F00000000000000000000000000000000",
            "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        ),
        "XRP",
    ): Market(
        id="534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/XRP",
        symbol=MarketSymbol(
            CurrencyCode(
                "534F4C4F00000000000000000000000000000000",
                "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
            ),
            "XRP",
        ),
        base=CurrencyCode(
            "534F4C4F00000000000000000000000000000000",
            "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        ),
        quote=CurrencyCode("XRP"),
    ),
    MarketSymbol(
        CurrencyCode(
            "434F524500000000000000000000000000000000",
            "rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
        ),
        "XRP",
    ): Market(
        id="434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D/XRP",
        symbol=MarketSymbol(
            CurrencyCode(
                "434F524500000000000000000000000000000000",
                "rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
            ),
            "XRP",
        ),
        base=CurrencyCode(
            "434F524500000000000000000000000000000000",
            "rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
        ),
        quote=CurrencyCode("XRP"),
    ),
    MarketSymbol(
        CurrencyCode(
            "434F524500000000000000000000000000000000",
            "rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
        ),
        CurrencyCode(
            "534F4C4F00000000000000000000000000000000",
            "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        ),
    ): Market(
        id="434F524500000000000000000000000000000000+rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D/534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        symbol=MarketSymbol(
            CurrencyCode(
                "434F524500000000000000000000000000000000",
                "rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
            ),
            CurrencyCode(
                "534F4C4F00000000000000000000000000000000",
                "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
            ),
        ),
        base=CurrencyCode(
            "434F524500000000000000000000000000000000",
            "rcoreNywaoz2ZCQ8Lg2EbSLnGuRBmun6D",
        ),
        quote=CurrencyCode(
            "534F4C4F00000000000000000000000000000000",
            "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        ),
    ),
    MarketSymbol(
        CurrencyCode(
            "534F4C4F00000000000000000000000000000000",
            "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        ),
        CurrencyCode("USD", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
    ): Market(
        id="534F4C4F00000000000000000000000000000000+rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz/USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
        symbol=MarketSymbol(
            CurrencyCode(
                "534F4C4F00000000000000000000000000000000",
                "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
            ),
            "USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
        ),
        base=CurrencyCode(
            "534F4C4F00000000000000000000000000000000",
            "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
        ),
        quote=CurrencyCode("USD", "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B"),
    ),
    MarketSymbol(
        "XRP", CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq")
    ): Market(
        id="XRP/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
        symbol=MarketSymbol(
            "XRP", CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq")
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
    ),
    MarketSymbol(
        "XRP", CurrencyCode("EUR", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq")
    ): Market(
        id="XRP/EUR+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
        symbol=MarketSymbol(
            "XRP", CurrencyCode("EUR", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq")
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode("EUR", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
    ),
    MarketSymbol(
        "XRP", CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc")
    ): Market(
        id="XRP/SGB+rctArjqVvTHihekzDeecKo6mkTYTUSBNc",
        symbol=MarketSymbol(
            "XRP", CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc")
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc"),
    ),
    MarketSymbol(
        "XRP", CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc")
    ): Market(
        id="XRP/ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h",
        symbol=MarketSymbol(
            "XRP", CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc")
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode("ETH", "rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h"),
    ),
    MarketSymbol(
        "XRP", CurrencyCode("XTK", "rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb")
    ): Market(
        id="XRP/XTK+rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb",
        symbol=MarketSymbol(
            "XRP", CurrencyCode("XTK", "rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb")
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode("XTK", "rXTKdHWuppSjkbiKoEv53bfxHAn1MxmTb"),
    ),
    MarketSymbol(
        "XRP",
        CurrencyCode(
            "5852646F67650000000000000000000000000000",
            "rLqUC2eCPohYvJCEBJ77eCCqVL2uEiczjA",
        ),
    ): Market(
        id="XRP/5852646F67650000000000000000000000000000+rLqUC2eCPohYvJCEBJ77eCCqVL2uEiczjA",
        symbol=MarketSymbol(
            "XRP",
            CurrencyCode(
                "5852646F67650000000000000000000000000000",
                "rLqUC2eCPohYvJCEBJ77eCCqVL2uEiczjA",
            ),
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode(
            "5852646F67650000000000000000000000000000",
            "rLqUC2eCPohYvJCEBJ77eCCqVL2uEiczjA",
        ),
    ),
    MarketSymbol(
        "XRP",
        CurrencyCode(
            "58464C4F4B490000000000000000000000000000",
            "rUtXeAXonpFpgKubAa7LxcLd7NFep92T1t",
        ),
    ): Market(
        id="XRP/58464C4F4B490000000000000000000000000000+rUtXeAXonpFpgKubAa7LxcLd7NFep92T1t",
        symbol=MarketSymbol(
            "XRP",
            CurrencyCode(
                "58464C4F4B490000000000000000000000000000",
                "rUtXeAXonpFpgKubAa7LxcLd7NFep92T1t",
            ),
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode(
            "58464C4F4B490000000000000000000000000000",
            "rUtXeAXonpFpgKubAa7LxcLd7NFep92T1t",
        ),
    ),
    MarketSymbol(
        "XRP",
        CurrencyCode(
            "4A554E4B00000000000000000000000000000000",
            "r4pDJ7bT1rANe9nAdFR9pyVRwtJZQUEFpj",
        ),
    ): Market(
        id="XRP/4A554E4B00000000000000000000000000000000+r4pDJ7bT1rANe9nAdFR9pyVRwtJZQUEFpj",
        symbol=MarketSymbol(
            "XRP",
            CurrencyCode(
                "4A554E4B00000000000000000000000000000000",
                "r4pDJ7bT1rANe9nAdFR9pyVRwtJZQUEFpj",
            ),
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode(
            "4A554E4B00000000000000000000000000000000",
            "r4pDJ7bT1rANe9nAdFR9pyVRwtJZQUEFpj",
        ),
    ),
    MarketSymbol(
        "XRP",
        CurrencyCode(
            "5844554445000000000000000000000000000000",
            "rU5LE7X6yyu9DuHsLdHhWSiUVTgpyRK1vz",
        ),
    ): Market(
        id="XRP/5844554445000000000000000000000000000000+rU5LE7X6yyu9DuHsLdHhWSiUVTgpyRK1vz",
        symbol=MarketSymbol(
            "XRP",
            CurrencyCode(
                "5844554445000000000000000000000000000000",
                "rU5LE7X6yyu9DuHsLdHhWSiUVTgpyRK1vz",
            ),
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode(
            "5844554445000000000000000000000000000000",
            "rU5LE7X6yyu9DuHsLdHhWSiUVTgpyRK1vz",
        ),
    ),
    MarketSymbol(
        "XRP",
        CurrencyCode(
            "457175696C69627269756D000000000000000000",
            "rpakCr61Q92abPXJnVboKENmpKssWyHpwu",
        ),
    ): Market(
        id="XRP/457175696C69627269756D000000000000000000+rpakCr61Q92abPXJnVboKENmpKssWyHpwu",
        symbol=MarketSymbol(
            "XRP",
            CurrencyCode(
                "457175696C69627269756D000000000000000000",
                "rpakCr61Q92abPXJnVboKENmpKssWyHpwu",
            ),
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode(
            "457175696C69627269756D000000000000000000",
            "rpakCr61Q92abPXJnVboKENmpKssWyHpwu",
        ),
    ),
    MarketSymbol(
        "XRP", CurrencyCode("ELS", "rHXuEaRYnnJHbDeuBH5w8yPh5uwNVh5zAg")
    ): Market(
        id="XRP/ELS+rHXuEaRYnnJHbDeuBH5w8yPh5uwNVh5zAg",
        symbol=MarketSymbol(
            "XRP", CurrencyCode("ELS", "rHXuEaRYnnJHbDeuBH5w8yPh5uwNVh5zAg")
        ),
        base=CurrencyCode("XRP"),
        quote=CurrencyCode("ELS", "rHXuEaRYnnJHbDeuBH5w8yPh5uwNVh5zAg"),
    ),
    MarketSymbol(
        CurrencyCode("BTC", "rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL"),
        CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
    ): Market(
        id="BTC+rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
        symbol=MarketSymbol(
            "BTC+rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL",
            CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
        ),
        base=CurrencyCode("BTC", "rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL"),
        quote=CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
    ),
    MarketSymbol(
        CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc"),
        CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
    ): Market(
        id="ETH+rcA8X3TVMST1n3CJeAdGk1RdRCHii7N2h/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq",
        symbol=MarketSymbol(
            CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc"),
            CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
        ),
        base=CurrencyCode("SGB", "rctArjqVvTHihekzDeecKo6mkTYTUSBNc"),
        quote=CurrencyCode("USD", "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"),
    ),
}
