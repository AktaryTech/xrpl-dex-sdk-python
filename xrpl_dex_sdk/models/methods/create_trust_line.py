from typing import Any, Dict, NamedTuple
from ..common import CurrencyCode

#
# Expected response from a create_trust_line call
#
# @category Responses
#
class CreateTrustLineResponse(NamedTuple):
    code: CurrencyCode
    amount: str
    info: Dict[str, Any]


__all__ = ["CreateTrustLineResponse"]
