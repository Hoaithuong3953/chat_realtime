from channels.generic.websocket import AsyncJsonWebsocketConsumer
from pydantic import ValidationError
from typing import Any

from shared.exceptions.base import AppException
from shared.exceptions.common import InternalServerException
from shared.logger import logging

from core.websocket.context import WebSocketContext
from core.websocket.events import WebSocketEvent
from core.websocket.exceptions import InvalidPayloadException, UnsupportedEventException
from core.websocket.base_handler import WebSocketHandler
from core.websocket.base_schema import WebSocketRequest, WebSocketResponse

logger = logging.getLogger(__name__)

class BaseConsumer(AsyncJsonWebsocketConsumer):

    handlers: dict[str, WebSocketHandler] = {}

    async def receive_json(
        self,
        content: dict[str, Any],
        **kwargs: Any,
    ) -> None:
        response = await self.handle_request(content)
        handled = await self.after_handle(response)

        if not handled:
            await self.send_event(response)

    async def handle_request(self, content: dict[str, Any]) -> WebSocketResponse:
        try:
            request = self.parse_request(content)
            context = self.build_context()

            return await self.execute_handler(
                context=context,
                request=request,
            )
        except Exception as exc:
            return self.build_error_response(exc)

    def parse_request(self, content: dict[str, Any]) -> WebSocketRequest:
        try:
            return WebSocketRequest.model_validate(content)
        except ValidationError as exc:
            raise InvalidPayloadException(details=exc.errors()) from exc

    async def execute_handler(
        self,
        context: WebSocketContext,
        request: WebSocketRequest,
    ) -> WebSocketResponse:
        handler = self.handlers.get(request.event)
        if handler is None:
            raise UnsupportedEventException()
        return await handler.handle(
            context=context,
            request=request,
        )

    async def after_handle(self, response: WebSocketResponse) -> bool:
        return False

    async def send_event(self, response: WebSocketResponse) -> None:
        await self.send_json(
            response.model_dump(mode="json")
        )

    def build_error_response(self, exc: Exception) -> WebSocketResponse:
        if isinstance(exc, AppException):
            error = exc
        else:
            logger.exception("Unhandled websocket exception")
            error = InternalServerException()

        return WebSocketResponse(
            event=WebSocketEvent.ERROR,
            data=error.to_dict(),
        )

    def build_context(self) -> WebSocketContext:
        raise NotImplementedError