from django.contrib import admin

from .models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "restaurant__name")
