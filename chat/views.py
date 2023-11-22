from django.http import HttpRequest, Http404
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from chat.models import ChatRoom, SystemPromp, ChatHistory
from chat.serializers import ChatRoomDto, CreateChatRoomDto, SystemPrompDto, ChatRoomInfoDto, ChatHistoryDto


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
            chat_room = ChatRoom.objects.create(user=request.user, name=serializer.data["name"])
            chat_room.save()
            SystemPromp.objects.create(content=serializer.data["system_prompt"], chat_room=chat_room).save()
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
            chat_history_serializer.data
        )

        data = {"chat_room": dto.chat_room, "system_prompt": dto.system_prompt, "chat_history": dto.chat_history}
        return Response(data, status=200)


class ChatHistoryApiView(APIView):
    http_method_names = ["get", 'post']
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            chat_room = get_object_or_404(ChatRoom.objects.all(), pk=kwargs.get("room_id"))
        except Http404:
            return Response({"message": "존재하지 않는 채팅방입니다."}, status=HTTP_404_NOT_FOUND)

        chat_history = ChatHistory.objects.filter(chat_room=chat_room)
        serializer = ChatHistoryDto(chat_history, many=True)
        data = {"data": serializer.data}
        return Response(data, status=200)

    def post(self, request, *args, **kwargs):
        pass
