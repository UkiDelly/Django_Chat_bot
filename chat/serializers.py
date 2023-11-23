from dataclasses import dataclass

from rest_framework import serializers

from chat.models import ChatRoom, ChatHistory, SystemPromp


class ChatRoomDto(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ["id", "name", "created_at"]

    # override the method that returns the data


class CreateChatRoomDto(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    system_prompt = serializers.CharField(max_length=None)


class SystemPrompDto(serializers.ModelSerializer):
    class Meta:
        model = SystemPromp
        fields = ["id", "content", "created_at"]


class CreateSystemPrompDto(serializers.Serializer):
    content = serializers.CharField(max_length=None)


class ChatHistoryDto(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory

        fields = ["id", "message", "role", "created_at"]


@dataclass
class ChatRoomInfoDto:
    chat_room: dict
    system_prompt: list[dict]
    chat_history: list[dict]
