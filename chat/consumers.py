import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        user: User = self.scope["user"]
        # if self.scope["user"].is_authenticated:  # self.scope["user"].is_anonymous:
        #     await self.close()
        # else:
        print(user.is_authenticated)
        await self.accept()
        await self.send("소켓 연결이 되었습니다.")

    async def receive_json(self, content, **kwargs):
        print(content)
        await self.send_json(content)

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content, ensure_ascii=False, )
