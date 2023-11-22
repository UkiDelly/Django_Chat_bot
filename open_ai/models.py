from abc import ABC
from dataclasses import dataclass
from typing import Literal, Final


@dataclass
class BaseModel(ABC):
    content: str
    role: Literal['user', 'system', 'assistant']

    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }


@dataclass
class UserMessage(BaseModel):
    content: str
    role: Final = 'user'


@dataclass
class SystemMessage(BaseModel):
    content: str
    role: Final = 'system'


@dataclass
class AssistantMessage(BaseModel):
    content: str
    role: Final = 'assistant'


class Message:
    def __init__(self, **json):
        self.role: str = json.get("role")
        self.content: str = json.get("content")

    def __str__(self):
        return f"Message(role={self.role}, content={self.content})"

    def __repr__(self):
        return str(self)


#
class Choice:
    def __init__(self, **json):
        self.index: int = json.get('index')
        self.message: Message = Message(**json.get('message'))
        self.finish_reason: str = json.get('finish_reason')

    def __str__(self):
        return f"Choice(index={self.index}, message={self.message}, finish_reason={self.finish_reason})"

    def __repr__(self):
        return str(self)


class Usage:
    def __init__(self, **json):
        self.completion_tokens: int = json.get('completion_tokens')
        self.prompt_tokens: int = json.get('prompt_tokens')
        self.total_tokens: int = json.get('total_tokens')

    def __str__(self):
        return f"Usage(completion_tokens={self.completion_tokens}, prompt_tokens={self.prompt_tokens}, total_tokens={self.total_tokens})"

    def __repr__(self):
        return str(self)


class OpenAiResponse:
    def __init__(self, **json):
        self.id: int = json.get('id')
        self.choice: list[Choice] = [Choice(**choice) for choice in json.get('choices')]
        self.model: str = json.get('model')
        self.created: int = json.get('created')
        self.system_fingerprint: str = json.get('system_fingerprint')
        self.object: str = json.get('object')
        self.usage: Usage = Usage(**json.get('usage'))

    def __str__(self):
        return f"OpenAiResponse(id={self.id}, choice={self.choice}, model={self.model}, created={self.created}, system_fingerprint={self.system_fingerprint}, object={self.object}, usage={self.usage})"

    def __repr__(self):
        return str(self)
