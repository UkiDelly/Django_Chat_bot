from dataclasses import dataclass

from rest_framework import serializers

from accounts.models import MyUser, MyTokenModel


class UserInfoDto(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'nickname', 'email', 'sns_id', 'social_type']


class MyTokenDto(serializers.Serializer):
    access_token = serializers.CharField
    refresh_token = serializers.CharField


@dataclass
class UserInfoWithTokenDto:
    user: MyUser
    token: MyTokenModel

    def to_json(self):
        return {"user": self.user.to_json(), "token": self.token.to_json()}


class RegisterDto(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"


class LoginDto(serializers.Serializer):
    email = serializers.EmailField()
    sns_id = serializers.CharField(allow_null=True, allow_blank=True)
    social_type = serializers.ChoiceField(choices=MyUser.SocialType.choices)
    password = serializers.CharField(allow_null=True, allow_blank=True)
