from xrpl.models.requests.server_state import ServerState
from xrpl.utils import ripple_time_to_posix

from ..models import (
    ExchangeStatusType,
    FetchStatusResponse,
)


def fetch_status(self) -> FetchStatusResponse:
    server_state_response = self.client.request(ServerState())
    server_state_result = server_state_response.result

    if "error" in server_state_result:
        print(server_state_result["error_message"])
        return

    server_state = server_state_result["state"]

    status = ExchangeStatusType.OK

    if server_state["server_state"] == "disconnected":
        status = ExchangeStatusType.SHUTDOWN

    return FetchStatusResponse(
        status=status.value,
        updated=ripple_time_to_posix,
        eta="",
        url="",
        info={"server_state": server_state},
    )
