from django.contrib import admin
from django.contrib.admin import register

from Api.models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "last_login",
    )
    list_filter = ("is_superuser",)
    search_fields = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "email",
    )
