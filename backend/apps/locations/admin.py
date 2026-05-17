from django.contrib import admin

from .models import Area, City, Country, Cuisine, Location


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "slug")
    list_filter = ("country",)
    search_fields = ("name", "slug", "country__name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "postcode_prefix", "latitude", "longitude")
    list_filter = ("city__country", "city")
    search_fields = ("name", "slug", "postcode_prefix", "city__name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "area", "postcode", "country")
    search_fields = ("country", "city", "area", "borough_or_district", "postcode")
