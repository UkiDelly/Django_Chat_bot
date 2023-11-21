# Create your models here.
from django.db import models


class BaseTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        abstract = True


class UserChat(BaseTime):
    user = models.ForeignKey("accounts.MyUser", on_delete=models.CASCADE)
    name = models.CharField()

    class Meta:
        db_table = "user_chat"


class ChatHistory(BaseTime):
    class Role(models.IntegerChoices):
        SYSTEM = 0
        USER = 1
        ASSISTANT = 2

    chat_room = models.ForeignKey("chat.UserChat", on_delete=models.CASCADE)
    message = models.TextField()
    role = models.IntegerField(choices=Role.choices)

    class Meta:
        db_table = "chat_history"
