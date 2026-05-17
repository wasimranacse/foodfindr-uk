from django.contrib import admin

from .models import FavouriteRestaurant


@admin.register(FavouriteRestaurant)
class FavouriteRestaurantAdmin(admin.ModelAdmin):
    list_display = ("customer", "restaurant", "created_at")
    search_fields = ("customer__email", "restaurant__name")
