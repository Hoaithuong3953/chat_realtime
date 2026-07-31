from pydantic import BaseModel, ConfigDict, Field
from typing import Any

from core.websocket.events import WebSocketEvent

class WebSocketRequest(BaseModel):
    """
    Common envelope for all incoming websocket messages
    """
    model_config = ConfigDict(frozen=True)

    event: WebSocketEvent = Field(description="Incoming websocket event")
    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Event payload",
    )

class WebSocketResponse(BaseModel):
    """
    Common envelope for all outgoing websocket messages
    """
    model_config = ConfigDict(frozen=True)

    event: WebSocketEvent = Field(default=WebSocketEvent.SUCCESS, description="Outgoing websocket event")
    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Response payload",
    )