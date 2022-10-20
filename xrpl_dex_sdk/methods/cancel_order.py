from xrpl.transaction import safe_sign_and_submit_transaction
from xrpl.models.transactions import OfferCancel

from ..models.ccxt.orders import OrderId
from ..models.methods.cancel_order import CancelOrderParams, CancelOrderResponse


def cancel_order(
    self, id: OrderId, params: CancelOrderParams = CancelOrderParams()
) -> CancelOrderResponse:
    offer_cancel_request = {
        "account": self.wallet.classic_address,
        "offer_sequence": id.sequence,
    }
    for field in params.__dataclass_fields__:
        if params.__getattribute__(field) != None:
            offer_cancel_request[field] = params.__getattribute__(field)

    offer_cancel_result = safe_sign_and_submit_transaction(
        transaction=OfferCancel.from_dict(offer_cancel_request),
        wallet=self.wallet,
        client=self.sync_client,
    )

    return CancelOrderResponse(id=id, info={"OfferCancel": offer_cancel_result})
