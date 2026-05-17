from django.contrib import admin

from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "approval_status", "created_at")
    list_filter = ("approval_status", "is_collection_available", "is_delivery_available")
    search_fields = ("name", "owner__email", "location__city", "location__postcode")
    prepopulated_fields = {"slug": ("name",)}
