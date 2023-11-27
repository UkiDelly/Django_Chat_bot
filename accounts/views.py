from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.models import MyUser, MyTokenModel
from accounts.serializers import (
    RegisterDto,
    UserInfoWithTokenDto,
    LoginDto,
    UserInfoDto,
    NicknameChangeDto,
)


class RegisterAPI(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = RegisterDto(data=request.data)

        if serializer.is_valid():
            user: MyUser = MyUser.objects.create_user(
                nickname=serializer.data["nickname"],
                email=serializer.data["email"],
                social_type=serializer.data["social_type"],
                sns_id=serializer.data["sns_id"],
                password=serializer.data["password"],

            )
            token_obj = TokenObtainPairSerializer.get_token(user)
            token = MyTokenModel(token_obj.access_token, token_obj)
            dto = UserInfoWithTokenDto(user, token)
            return Response(dto.to_json(), status=201)
        else:
            return Response(serializer.errors, status=400)


class LoginAPI(APIView):
    http_method_names = ["post"]

    def post(self, request: HttpRequest):
        serializer = LoginDto(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(MyUser, email=serializer.data["email"])
            user.last_login = datetime.now()
            token_obj = TokenObtainPairSerializer.get_token(user)
            token = MyTokenModel(token_obj.access_token, token_obj)
            dto = UserInfoWithTokenDto(user, token)
            return Response(dto.to_json(), status=200)
        else:
            return Response(serializer.errors, status=400)


class MyInfoAPI(APIView):
    http_method_names = ["get", "patch"]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        dto = UserInfoDto(user)
        return Response(dto.data, status=200)

    def patch(self, request: HttpRequest):
        serializer = NicknameChangeDto(data=request.data)

        if serializer.is_valid():
            user = request.user
            user.nickname = serializer.data["nickname"]
            user.save()
            return Response(UserInfoDto(user).data, status=200)

        else:
            return Response(serializer.errors, status=400)


class AutoLoginAPI(TokenRefreshView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        # access_token 토큰 발급이 정상적으로 완료 되었을때
        if response.status_code == 200:
            access_token = response.data.get("access")

            # access_token를 검증하여 user_id를 추출
            user_id = AccessToken(access_token)["user_id"]
            user = get_object_or_404(MyUser, pk=user_id)

            # 유저 정보를 가져와서 직렬화
            user_data = UserInfoDto(user).data

            # response의 data를 벼경
            data = {"user": user_data, "access_token": access_token}
            response.data = data

        return response
