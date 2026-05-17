from django.contrib import admin

from .models import Favourite


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ("customer", "restaurant", "created_at")
    search_fields = ("customer__email", "restaurant__name")
