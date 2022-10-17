from xrpl.transaction import safe_sign_and_submit_transaction
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.transactions import TrustSet

from ..models.common import CurrencyCode
from ..models.methods.create_trust_line import CreateTrustLineResponse


def create_trust_line(
    self, code: CurrencyCode, limit_amount: str
) -> CreateTrustLineResponse:
    if code.code == "XRP":
        raise Exception("Error creating Trust Line: No line needed for XRP")
    elif code.issuer == None:
        raise Exception("Error creating Trust Line: Invalid code")

    trust_set_request = {
        "account": self.wallet.classic_address,
        "limit_amount": IssuedCurrencyAmount(
            currency=code.currency,
            issuer=code.issuer,
            value=limit_amount,
        ),
    }
    trust_set_result = safe_sign_and_submit_transaction(
        transaction=TrustSet.from_dict(trust_set_request),
        wallet=self.wallet,
        client=self.client,
    )

    return CreateTrustLineResponse(
        code=code, amount=limit_amount, info={"TrustSet": trust_set_result}
    )
