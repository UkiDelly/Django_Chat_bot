from django.contrib import admin

from accounts.models import MyUser


# Register your models here.
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ["nickname", "email", "social_type", "created_at"]
    list_filter = ['social_type']
    readonly_fields = ['password']
    search_fields = ['nickname', 'email', 'social_type']
    ordering = ['created_at', 'social_type']
