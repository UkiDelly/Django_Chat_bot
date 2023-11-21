from django.http import HttpRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chat.models import ChatRoom
from chat.serializers import ChatRoomDto, CreateChatRoomDto


# Create your views here.
class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomDto

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = CreateChatRoomDto(data=request.data)

        if serializer.is_valid():
            chat_room = ChatRoom.objects.create(user=request.user, name=serializer.data["name"])
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
