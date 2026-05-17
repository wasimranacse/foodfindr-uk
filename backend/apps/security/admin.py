from django.contrib import admin

from .models import EmailVerificationCode, PasswordResetCode, SecurityAuditLog


@admin.register(SecurityAuditLog)
class SecurityAuditLogAdmin(admin.ModelAdmin):
    list_display = ("event_type", "user", "ip_address", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("user__email", "ip_address", "user_agent")
    readonly_fields = ("created_at",)


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "purpose", "attempts", "is_used", "expires_at", "created_at")
    list_filter = ("purpose", "is_used", "created_at")
    search_fields = ("user__email",)
    readonly_fields = ("code_hash", "created_at")


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "attempts", "is_used", "expires_at", "created_at")
    list_filter = ("is_used", "created_at")
    search_fields = ("user__email",)
    readonly_fields = ("code_hash", "created_at")
