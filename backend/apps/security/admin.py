from django.contrib import admin

from .models import SecurityAuditLog


@admin.register(SecurityAuditLog)
class SecurityAuditLogAdmin(admin.ModelAdmin):
    list_display = ("event_type", "user", "ip_address", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("user__email", "ip_address", "user_agent")
    readonly_fields = ("created_at",)
