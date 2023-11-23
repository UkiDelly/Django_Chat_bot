from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat.views import ChatRoomViewSet, ChatHistoryApiView, SystemPrompViewSet

chat_router = DefaultRouter()
chat_router.register("", ChatRoomViewSet)

chat_system_router = DefaultRouter()
chat_system_router.register("system", SystemPrompViewSet)

urlpatterns = [
    path("", include(chat_router.urls)),
    path("<int:room_id>/history/", ChatHistoryApiView.as_view()),
    path("<int:room_id>/", include(chat_system_router.urls)),
]
