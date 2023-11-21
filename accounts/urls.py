from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import RegisterAPI, LoginAPI, MyInfoAPI

urlpatterns = [
    path("register/", RegisterAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("myinfo/", MyInfoAPI.as_view()),
    path("", include("dj_rest_auth.urls")),
]
