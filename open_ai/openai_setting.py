import asyncio

from openai import AsyncOpenAI

from chatbot.settings import env
from open_ai.models import SystemMessage, AssistantMessage, UserMessage


class MyOpenAiClient():
    def __init__(self, *sytems: SystemMessage, history: list[UserMessage | AssistantMessage] = []):
        self.client = AsyncOpenAI(
            api_key=env("OPEN_AI"))
        self.sytem_promp = sytems
        self.history = history
        self.new_conversation: list[UserMessage | AssistantMessage] = []

    def set_system(self, *promp: SystemMessage):
        self.sytem_promp = promp

    def add_new_user_message(self, message: str):
        user_message = UserMessage(message)
        self.new_conversation.append(user_message)

    def get_conversations(self):
        return self.history + self.new_conversation

    async def send(self):
        res = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[msg.to_dict() for msg in self.get_conversations()]
        )

        print(res)


async def async_main():
    client = MyOpenAiClient(SystemMessage("너는 파이썬 전문가야"))
    client.add_new_user_message("파이썬에 대해 알려줘")
    await client.send()


if __name__ == '__main__':
    asyncio.run(async_main())
