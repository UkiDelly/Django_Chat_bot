from django.urls import path, include

from accounts.views import RegisterView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("register/", RegisterView.as_view()),
    # path("login/", LoginApi.as_view()),
]
