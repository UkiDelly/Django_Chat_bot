import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from accounts.models import MyUser


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        user: MyUser = self.scope["user"]
        print(user)
        if user.is_authenticated:
            await self.accept()
            await self.send("소켓 연결이 되었습니다.")
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.send("소켓 연결이 종료되었습니다.")

    async def receive_json(self, content, **kwargs):
        print(content)
        await self.send_json(content)

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content, ensure_ascii=False, )
