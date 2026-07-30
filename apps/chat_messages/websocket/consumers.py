from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]

        await self.accept()

        await self.send_json({
            "event": "CONNECTED",
            "chat_id": str(self.chat_id),
        })

    async def disconnect(self, close_code):
        pass

    async def receive_json(self, content, **kwargs):
        await self.send_json(content)