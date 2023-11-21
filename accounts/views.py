from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import MyUser, MyTokenModel
from accounts.serializers import RegisterDto, UserInfoWithTokenDto, LoginDto, UserInfoDto


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
