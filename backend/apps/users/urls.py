from django.urls import path

from .views import (
    CustomerRegistrationView,
    LoginView,
    LogoutView,
    OwnerRegistrationView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    PasswordResetVerifyView,
    ProfileView,
    RefreshTokenView,
    ResendVerificationCodeView,
    VerifyEmailView,
)

urlpatterns = [
    path("register/customer/", CustomerRegistrationView.as_view(), name="register-customer"),
    path("register/owner/", OwnerRegistrationView.as_view(), name="register-owner"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path(
        "resend-verification-code/",
        ResendVerificationCodeView.as_view(),
        name="resend-verification-code",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "password-reset/request/",
        PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/verify/",
        PasswordResetVerifyView.as_view(),
        name="password-reset-verify",
    ),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
