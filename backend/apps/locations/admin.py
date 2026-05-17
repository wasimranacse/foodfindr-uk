from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "area", "postcode", "country")
    search_fields = ("country", "city", "area", "borough_or_district", "postcode")
