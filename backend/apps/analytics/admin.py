from django.contrib import admin

from .models import LocationSearchLog, RestaurantAnalyticsEvent


@admin.register(RestaurantAnalyticsEvent)
class RestaurantAnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "restaurant", "customer", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("restaurant__name", "customer__email")
    readonly_fields = ("created_at",)


@admin.register(LocationSearchLog)
class LocationSearchLogAdmin(admin.ModelAdmin):
    list_display = ("query", "postcode", "customer", "created_at")
    search_fields = ("query", "postcode", "customer__email")
    readonly_fields = ("created_at",)
