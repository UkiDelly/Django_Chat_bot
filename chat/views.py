from django.http import HttpRequest, Http404
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chat.models import ChatRoom, SystemPromp, ChatHistory
from chat.serializers import (
    ChatRoomDto,
    CreateChatRoomDto,
    SystemPrompDto,
    ChatRoomInfoDto,
    ChatHistoryDto,
    CreateSystemPrompDto,
)


# Create your views here.
class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomDto

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def list(self, request: HttpRequest, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"chat_rooms": serializer.data}, status=200)

    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = CreateChatRoomDto(data=request.data)

        if serializer.is_valid():
            chat_room = ChatRoom.objects.create(
                user=request.user, name=serializer.data["name"]
            )
            chat_room.save()
            serializer = ChatRoomDto(chat_room)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def retrieve(self, request: HttpRequest, *args, **kwargs):
        instance = self.get_object()
        instance_serializer = self.get_serializer(instance)

        promps = SystemPromp.objects.filter(chat_room=instance)
        promps_serializer = SystemPrompDto(promps, many=True)

        chat_history = ChatHistory.objects.filter(chat_room=instance)
        chat_history_serializer = ChatHistoryDto(chat_history, many=True)

        dto = ChatRoomInfoDto(
            instance_serializer.data,
            promps_serializer.data,
            chat_history_serializer.data,
        )

        data = {
            "chat_room": dto.chat_room,
            "system_prompt": dto.system_prompt,
            "chat_history": dto.chat_history,
        }
        return Response(data, status=200)


class ChatHistoryApiView(ListAPIView):
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistoryDto
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_room = get_object_or_404(ChatRoom, pk=self.kwargs["room_id"])
        return self.queryset.filter(chat_room=chat_room)


class SystemPrompViewSet(ModelViewSet):
    queryset = SystemPromp.objects.all()
    serializer_class = SystemPrompDto
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_room = get_object_or_404(ChatRoom, pk=self.kwargs["room_id"])
        return self.queryset.filter(chat_room=chat_room)

    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = CreateSystemPrompDto(data=request.data)

        if serializer.is_valid():
            try:
                chat_room = get_object_or_404(ChatRoom, pk=self.kwargs["room_id"])
            except Http404:
                return Response({"message": "채탕 채팅룸을 찾을 수 없습니다."}, status=404)
            SystemPromp.objects.create(
                content=serializer.data["content"], chat_room=chat_room
            ).save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
