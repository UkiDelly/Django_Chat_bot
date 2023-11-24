from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from chatbot.settings import env
from open_ai.models import SystemMessage, AssistantMessage, UserMessage


class MyOpenAiClient():
    def __init__(self, ):
        self.client = AsyncOpenAI(
            api_key=env("OPEN_AI"))
        self.sytem_promp: list = []
        self.history: list = []
        self.new_conversation: list[UserMessage | AssistantMessage] = []

    def set_system(self, *promp: SystemMessage):
        self.sytem_promp = list(promp)

    def set_hitsory(self, history: list[UserMessage | AssistantMessage]):
        self.history = history

    def add_new_user_message(self, message: str):
        user_message = UserMessage(message)
        self.new_conversation.append(user_message)

    def get_conversations(self):
        new_list = self.sytem_promp + self.history + self.new_conversation
        return new_list

    async def send(self) -> AssistantMessage:
        res: ChatCompletion = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[msg.to_dict() for msg in self.get_conversations()]
        )

        return AssistantMessage(res.choices[0].message.content)

# async def async_main():
#     client = MyOpenAiClient(SystemMessage("너는 파이썬 전문가야"))
#     client.add_new_user_message("파이썬에 대해 알려줘")
#     await client.send()

#
# if __name__ == '__main__':
#     asyncio.run(async_main())
