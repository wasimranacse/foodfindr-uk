from django.contrib import admin

from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "restaurant", "is_active", "starts_at", "ends_at")
    list_filter = ("is_active",)
    search_fields = ("title", "restaurant__name")
