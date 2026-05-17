from django.contrib import admin

from .models import MenuCategory, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "restaurant__name")
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "category", "price", "is_available")
    list_filter = (
        "is_available",
        "is_halal",
        "is_vegan",
        "is_vegetarian",
        "is_gluten_free",
    )
    search_fields = ("name", "restaurant__name", "category__name")
