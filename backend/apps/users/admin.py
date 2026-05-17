from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class FoodFindrUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("FoodFindr", {"fields": ("role", "is_email_verified")}),
    )
    list_display = ("username", "email", "role", "is_email_verified", "is_staff")
    list_filter = UserAdmin.list_filter + ("role", "is_email_verified")
    search_fields = ("username", "email")
