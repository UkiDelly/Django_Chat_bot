from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from accounts.serializers import RegisterRequestSerializer, UserInfoWithTokenSerializer, UserInfoSerializer


class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            # JWT 발급
            token: Token = TokenObtainPairSerializer.get_token(user)
            user_info = UserInfoSerializer(data=serializer.data)
            user_info.is_valid()
            user_info_with_token = UserInfoWithTokenSerializer(
                data={"user": user_info.data, "access_token": str(token.access_token), "refresh_token": str(token)})
            user_info_with_token.is_valid()
            return Response(user_info_with_token.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
# class LoginApi(APIView):
#     http_method_names = ['post']
#
#     def post(self, request: HttpRequest):
#         body = json.loads(request.body)
#
#         if body.get('social_type') == 'email':
#             serializer = EmailLoginSerializer(data=body)
#             user = MyUser.objects.get(email=serializer.validated_data['email'])
#         else:
#             serializer = GoogleLoginSerializer(data=body)
#             user = MyUser.objects.get(sns_id=serializer.validated_data['sns_id'],
#                                       social_type=serializer.validated_data['social_type'],
#                                       email=serializer.validated_data['email'])
#
#             get_token_model()
#         if serializer.is_valid(raise_exception=True):
#
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
