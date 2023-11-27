from accounts.models import MyUser


def reset_chat_count():
    MyUser.objects.update(chat_count=0)
