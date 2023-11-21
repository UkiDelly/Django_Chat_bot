from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from accounts.models import MyUser

User: MyUser = get_user_model()


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "email", "sns_id", "social_type"]


class RegisterRequestSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "email", "password", "sns_id", "social_type"]

    def create(self, validated_data: dict):
        nickname = validated_data.get("nickname")
        email = validated_data.get("email")
        social_type = validated_data.get("social_type")
        password = validated_data.get("password", None)
        sns_id = validated_data.get("sns_id", None)

        user: MyUser = User.objects.create_user(
            nickname=nickname,
            email=email,
            sns_id=sns_id
        )
        if password:
            user.set_password(password)
        return user


class UserInfoWithTokenSerializer(Serializer):
    user = UserInfoSerializer()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
