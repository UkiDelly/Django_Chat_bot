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
