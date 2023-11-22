from tokenize import TokenError

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class WebSocketJWTAuthMiddleWare(BaseMiddleware):
    """
    웹소켓에서 JWT 토큰으로 인증하기 위해 만든 커스텀 미들웨어
    """

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):

        # headers에서 'authorization' 뽑아오기
        authorization_header = next(
            (header for header in scope["headers"] if header[0] == b"authorization"), None
        )

        if authorization_header:

            # Authorization: Bearer xxxxx 에서 Bearer을 제거하고 토큰값만 추출
            token = (authorization_header[1].decode("utf-8").split(" ")[-1])
        else:
            token = None

        try:
            # 추출한 토큰값을 검증
            access_token = AccessToken(token)
            scope["user"] = await get_user(access_token["user_id"])
        except TokenError:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
