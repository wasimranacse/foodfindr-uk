from django.contrib import admin

from .models import Restaurant, RestaurantOpeningHour


class RestaurantOpeningHourInline(admin.TabularInline):
    model = RestaurantOpeningHour
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "city",
        "area",
        "is_approved",
        "is_verified",
        "is_featured",
        "is_premium",
        "average_rating",
        "trust_score",
    )
    list_filter = (
        "is_approved",
        "is_verified",
        "is_featured",
        "is_premium",
        "delivery_available",
        "collection_available",
        "dine_in_available",
        "city",
    )
    search_fields = ("name", "owner__email", "city__name", "area__name", "postcode")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("cuisine_types",)
    inlines = [RestaurantOpeningHourInline]


@admin.register(RestaurantOpeningHour)
class RestaurantOpeningHourAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "day_of_week", "opening_time", "closing_time", "is_closed")
    list_filter = ("day_of_week", "is_closed")
    search_fields = ("restaurant__name",)
