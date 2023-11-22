import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from accounts.models import MyUser
from chat.utils import *


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user: MyUser = self.scope["user"]
        if user.is_authenticated:
            room_id = self.scope["url_route"]["kwargs"]["room_id"]
            chat_room = await get_chat_room(room_id)

            if chat_room is None:
                await self.close()
                return
            else:
                await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.send("소켓 연결이 종료되었습니다.")

    async def receive_json(self, content, **kwargs):
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        user_message = await convert_message(content)
        await add_chat_history(room_id, user_message.content, 1)
        await ask_gpt(room_id)
        await self.send_json({})

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content, ensure_ascii=False, )
