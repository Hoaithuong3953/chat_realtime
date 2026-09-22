from uuid import UUID
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class MessageBroadcaster:

    @staticmethod
    async def broadcast(chat_id: UUID, message: dict) -> None:
        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            f"chat_{chat_id}",
            {
                "type": "chat.message",
                "message": message,
            }
        )

    @staticmethod
    def broadcast_sync(chat_id: UUID, message: dict) -> None:
        async_to_sync(MessageBroadcaster.broadcast)(
            chat_id=chat_id,
            message=message,
        )