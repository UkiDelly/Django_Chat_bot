from rest_framework import serializers

from chat.models import ChatRoom, ChatHistory


class ChatRoomDto(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ["id", "name", "created_at"]

    # override the method that returns the data


class CreateChatRoomDto(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class ChatHistoryDto(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ["id", "name", "created_at"]
