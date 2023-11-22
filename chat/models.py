# Create your models here.
from django.db import models


class BaseTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ChatRoom(BaseTime):
    user = models.ForeignKey("accounts.MyUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "chat_room"


class ChatHistory(BaseTime):
    class Role(models.IntegerChoices):
        USER = 1
        ASSISTANT = 2

    chat_room = models.ForeignKey("chat.ChatRoom", on_delete=models.CASCADE)
    message = models.TextField()
    role = models.IntegerField(choices=Role.choices)

    class Meta:
        db_table = "chat_history"


class SystemPromp(models.Model):
    chat_room = models.ForeignKey("chat.ChatRoom", on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        db_table = "system_prompt"
