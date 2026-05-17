from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomerProfile, RestaurantOwnerProfile, User


@admin.register(User)
class FoodFindrUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "full_name",
        "role",
        "is_email_verified",
        "is_phone_verified",
        "is_active",
        "is_staff",
    )
    list_filter = (
        "role",
        "is_email_verified",
        "is_phone_verified",
        "is_active",
        "is_staff",
    )
    search_fields = ("email", "full_name", "phone")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "phone")}),
        (
            "FoodFindr",
            {
                "fields": (
                    "role",
                    "is_email_verified",
                    "is_phone_verified",
                    "failed_login_attempts",
                    "locked_until",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "postcode", "preferred_price_level")
    search_fields = ("user__email", "city", "postcode")


@admin.register(RestaurantOwnerProfile)
class RestaurantOwnerProfileAdmin(admin.ModelAdmin):
    list_display = ("business_name", "user", "business_email", "verification_status")
    list_filter = ("verification_status",)
    search_fields = ("business_name", "user__email", "business_email")
