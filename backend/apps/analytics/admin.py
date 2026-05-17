from django.contrib import admin

from .models import AnalyticsEvent


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "restaurant", "user", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("restaurant__name", "user__email")
    readonly_fields = ("created_at",)
