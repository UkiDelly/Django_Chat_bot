from rest_framework import serializers

from chat.models import ChatRoom


class ChatRoomDto(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"


class CreateChatRoomDto(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ["name"]
