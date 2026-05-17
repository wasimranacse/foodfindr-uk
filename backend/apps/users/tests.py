from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.security.models import EmailVerificationCode, SecurityAuditLog
from apps.security.services import (
    MAX_CODE_ATTEMPTS,
    create_email_verification_code,
    verify_email_code,
    VerificationError,
)

User = get_user_model()


class OTPServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="customer@example.com",
            password="StrongPass123!",
            full_name="Test Customer",
        )

    @patch("apps.security.services.generate_otp_code", return_value="123456")
    def test_otp_generation_stores_only_hash(self, _mock_code):
        create_email_verification_code(
            self.user,
            EmailVerificationCode.Purpose.REGISTRATION,
            enforce_cooldown=False,
        )

        verification = EmailVerificationCode.objects.get(user=self.user)

        self.assertNotEqual(verification.code_hash, "123456")
        self.assertTrue(check_password("123456", verification.code_hash))
        self.assertEqual(
            verification.expires_at.date(),
            (timezone.now() + timezone.timedelta(minutes=10)).date(),
        )


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
        "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
        "DEFAULT_THROTTLE_CLASSES": (),
        "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    }
)
class AuthAPITests(APITestCase):
    def setUp(self):
        cache.clear()

    def register_customer(self, email="new@example.com", password="StrongPass123!"):
        with patch("apps.security.services.generate_otp_code", return_value="123456"):
            return self.client.post(
                reverse("register-customer"),
                {
                    "email": email,
                    "password": password,
                    "full_name": "New Customer",
                    "city": "London",
                    "postcode": "SW1A 1AA",
                },
                format="json",
            )

    def test_register_customer_creates_hashed_verification_code(self):
        response = self.register_customer()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("123456", str(response.data))
        user = User.objects.get(email="new@example.com")
        verification = EmailVerificationCode.objects.get(user=user)
        self.assertTrue(check_password("123456", verification.code_hash))
        self.assertFalse(verification.is_used)
        self.assertTrue(
            SecurityAuditLog.objects.filter(
                user=user,
                event_type=SecurityAuditLog.EventType.REGISTRATION,
            ).exists()
        )

    def test_verify_email_success_marks_user_verified(self):
        self.register_customer()

        response = self.client.post(
            reverse("verify-email"),
            {"email": "new@example.com", "code": "123456"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(email="new@example.com")
        self.assertTrue(user.is_email_verified)
        self.assertTrue(
            SecurityAuditLog.objects.filter(
                user=user,
                event_type=SecurityAuditLog.EventType.VERIFICATION_SUCCESS,
            ).exists()
        )

    def test_expired_code_cannot_verify(self):
        self.register_customer()
        user = User.objects.get(email="new@example.com")
        EmailVerificationCode.objects.filter(user=user).update(
            expires_at=timezone.now() - timezone.timedelta(seconds=1)
        )

        with self.assertRaises(VerificationError):
            verify_email_code(
                user,
                "123456",
                EmailVerificationCode.Purpose.REGISTRATION,
            )
        user.refresh_from_db()
        self.assertFalse(user.is_email_verified)

    def test_failed_attempts_are_limited(self):
        self.register_customer()
        user = User.objects.get(email="new@example.com")

        for _ in range(MAX_CODE_ATTEMPTS):
            response = self.client.post(
                reverse("verify-email"),
                {"email": "new@example.com", "code": "000000"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        verification = EmailVerificationCode.objects.get(user=user)
        self.assertEqual(verification.attempts, MAX_CODE_ATTEMPTS)

        with self.assertRaises(VerificationError):
            verify_email_code(
                user,
                "123456",
                EmailVerificationCode.Purpose.REGISTRATION,
            )
        user.refresh_from_db()
        self.assertFalse(user.is_email_verified)

    def test_login_before_email_verification_is_restricted(self):
        self.register_customer()

        response = self.client.post(
            reverse("login"),
            {"email": "new@example.com", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["detail"][0]),
            "Please verify your email before logging in.",
        )

    def test_login_after_verification_returns_tokens(self):
        self.register_customer()
        self.client.post(
            reverse("verify-email"),
            {"email": "new@example.com", "code": "123456"},
            format="json",
        )

        response = self.client.post(
            reverse("login"),
            {"email": "new@example.com", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
