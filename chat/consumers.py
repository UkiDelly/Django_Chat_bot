from channels.generic.websocket import *

from chat.utils import *
from open_ai.openai_setting import MyOpenAiClient


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.client = MyOpenAiClient()
        super().__init__()

    async def connect(self):
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        chat_room = await get_chat_room(room_id)

        if chat_room is None:
            await self.close()
            return
        else:
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        print(text_data)
        user_message = await convert_message(text_data)
        add_res = await add_chat_history(room_id, user_message.content, 1)

        if not add_res:
            await self.close()
            return

        res = await ask_gpt(room_id, self.client)
        print(res)
        await self.send(res)
