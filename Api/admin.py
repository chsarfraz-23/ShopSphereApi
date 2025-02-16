from django.contrib import admin
from django.contrib.admin import register

from Api.models import User, ProductType, Product


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


@register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
        "modified_at",
        "created_by",
    )
    list_filter = ("is_active",)
    search_fields = (
        "is",
        "name",
        "created_by__username",
        "created_by__id",
    )
    list_select_related = ("created_by", "modified_by",)


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_active",
        "price",
        "discount",
        "city",
        "country",
        "email",
        "phone_number",
        "type",
        "created_at",
        "modified_at"
    )
    search_fields = (
        "id",
        "name",
        "price",
        "country",
        "city",
        "state",
        "email",
        "phone_number",
        "type__id",
        "type__name",
    )
    list_filter = ("is_active",)
    list_select_related = ("type",)
