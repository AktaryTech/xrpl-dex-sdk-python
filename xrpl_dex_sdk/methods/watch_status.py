from typing import Any, Dict
import uuid
from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models import StreamParameter, Subscribe

from ..models import WatchStatusParams


async def watch_status(self, params: WatchStatusParams) -> None:
    """
    Listens for updates regarding exchange status.

    Parameters
    ----------
    params : xrpl_dex_sdk.models.WatchStatusParams
        Additional request parameters
    """

    if isinstance(self.websocket_client, AsyncWebsocketClient) == False:
        raise Exception("Error watching balance: Websockets client not initialized")

    payload = Subscribe(
        id=uuid.uuid4().hex,
        streams=[StreamParameter.LEDGER],
    )

    async with self.websocket_client as websocket:
        await websocket.send(payload)
        initialized = False
        async for message in websocket:
            if initialized is False:
                if message.get("status") == "success":
                    initialized = True
                    continue
                else:
                    raise Exception(message)

            new_status = await self.fetch_status()
            if new_status != None:
                if isinstance(params, Dict):
                    params.listener(new_status)
                else:
                    params.listener(new_status)
