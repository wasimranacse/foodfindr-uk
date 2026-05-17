from django.contrib import admin

from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "restaurant", "offer_type", "is_active", "is_featured", "start_date", "end_date")
    list_filter = ("offer_type", "is_active", "is_featured")
    search_fields = ("title", "restaurant__name")
