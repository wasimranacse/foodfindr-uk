import secrets
from dataclasses import dataclass

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from .models import EmailVerificationCode, PasswordResetCode, SecurityAuditLog

CODE_TTL_MINUTES = 10
MAX_CODE_ATTEMPTS = 5
RESEND_COOLDOWN_SECONDS = 60


class VerificationError(Exception):
    pass


class CooldownError(VerificationError):
    pass


@dataclass(frozen=True)
class RequestContext:
    ip_address: str | None = None
    user_agent: str = ""


def get_request_context(request) -> RequestContext:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    ip_address = forwarded_for.split(",")[0].strip() if forwarded_for else None
    ip_address = ip_address or request.META.get("REMOTE_ADDR")
    return RequestContext(
        ip_address=ip_address,
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )


def audit_log(user, event_type, request=None, metadata=None) -> None:
    context = get_request_context(request) if request else RequestContext()
    SecurityAuditLog.objects.create(
        user=user,
        event_type=event_type,
        ip_address=context.ip_address,
        user_agent=context.user_agent,
        metadata=metadata or {},
    )


def generate_otp_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def _ensure_resend_allowed(model, user, purpose=None) -> None:
    filters = {"user": user, "is_used": False}
    if purpose is not None:
        filters["purpose"] = purpose
    latest_code = model.objects.filter(**filters).order_by("-created_at").first()
    if not latest_code:
        return
    cooldown_until = latest_code.created_at + timezone.timedelta(
        seconds=RESEND_COOLDOWN_SECONDS
    )
    if timezone.now() < cooldown_until:
        raise CooldownError("Please wait before requesting another code.")


def create_email_verification_code(user, purpose, *, enforce_cooldown=True) -> None:
    if enforce_cooldown:
        _ensure_resend_allowed(EmailVerificationCode, user, purpose)

    code = generate_otp_code()
    with transaction.atomic():
        EmailVerificationCode.objects.filter(
            user=user,
            purpose=purpose,
            is_used=False,
        ).update(is_used=True)
        EmailVerificationCode.objects.create(
            user=user,
            purpose=purpose,
            code_hash=make_password(code),
            expires_at=timezone.now() + timezone.timedelta(minutes=CODE_TTL_MINUTES),
        )

    send_mail(
        subject="Your FoodFindr verification code",
        message=f"Your FoodFindr verification code is {code}. It expires in 10 minutes.",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=True,
    )


def verify_email_code(user, code, purpose) -> None:
    verification = (
        EmailVerificationCode.objects.filter(
            user=user,
            purpose=purpose,
            is_used=False,
        )
        .order_by("-created_at")
        .first()
    )
    if not verification:
        raise VerificationError("Invalid or expired code.")
    if verification.expires_at <= timezone.now():
        verification.is_used = True
        verification.save(update_fields=["is_used"])
        raise VerificationError("Invalid or expired code.")
    if verification.attempts >= MAX_CODE_ATTEMPTS:
        raise VerificationError("Invalid or expired code.")

    if not check_password(code, verification.code_hash):
        verification.attempts += 1
        verification.save(update_fields=["attempts"])
        raise VerificationError("Invalid or expired code.")

    verification.is_used = True
    verification.save(update_fields=["is_used"])


def create_password_reset_code(user, *, enforce_cooldown=True) -> None:
    if enforce_cooldown:
        _ensure_resend_allowed(PasswordResetCode, user)

    code = generate_otp_code()
    with transaction.atomic():
        PasswordResetCode.objects.filter(user=user, is_used=False).update(is_used=True)
        PasswordResetCode.objects.create(
            user=user,
            code_hash=make_password(code),
            expires_at=timezone.now() + timezone.timedelta(minutes=CODE_TTL_MINUTES),
        )

    send_mail(
        subject="Your FoodFindr password reset code",
        message=f"Your FoodFindr password reset code is {code}. It expires in 10 minutes.",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=True,
    )


def verify_password_reset_code(user, code, *, consume=False) -> None:
    reset_code = (
        PasswordResetCode.objects.filter(user=user, is_used=False)
        .order_by("-created_at")
        .first()
    )
    if not reset_code:
        raise VerificationError("Invalid or expired code.")
    if reset_code.expires_at <= timezone.now():
        reset_code.is_used = True
        reset_code.save(update_fields=["is_used"])
        raise VerificationError("Invalid or expired code.")
    if reset_code.attempts >= MAX_CODE_ATTEMPTS:
        raise VerificationError("Invalid or expired code.")

    if not check_password(code, reset_code.code_hash):
        reset_code.attempts += 1
        reset_code.save(update_fields=["attempts"])
        raise VerificationError("Invalid or expired code.")

    if consume:
        reset_code.is_used = True
        reset_code.save(update_fields=["is_used"])
