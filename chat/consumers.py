from channels.generic.websocket import *

from chat.utils import *
from open_ai.openai_setting import MyOpenAiClient


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.client = MyOpenAiClient()
        super().__init__()

    async def connect(self):
        # user: MyUser = self.scope["user"]
        # if user.is_authenticated:
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        chat_room = await get_chat_room(room_id)

        if chat_room is None:
            await self.close()
            return
        else:
            await self.accept()
        # else:
        #     await self.close()

    async def disconnect(self, close_code):
        await self.send("소켓 연결이 종료되었습니다.")

    # async def receive_json(self, content, **kwargs):
    #     room_id = self.scope["url_route"]["kwargs"]["room_id"]
    #
    #     print(content)
    #     print(type(content))
    #     user_message = await convert_message(content)
    #     await add_chat_history(room_id, user_message.content, 1)
    #     res = await ask_gpt(room_id, self.client)
    #     await self.send_json(res.__dict__)

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
