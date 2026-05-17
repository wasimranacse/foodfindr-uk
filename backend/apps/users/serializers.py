from django.contrib.auth import authenticate, get_user_model, password_validation
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.security.models import EmailVerificationCode, SecurityAuditLog
from apps.security.services import (
    CooldownError,
    VerificationError,
    audit_log,
    create_email_verification_code,
    create_password_reset_code,
    verify_email_code,
    verify_password_reset_code,
)

from .models import CustomerProfile, RestaurantOwnerProfile, User

UserModel = get_user_model()


class CustomerRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    full_name = serializers.CharField(max_length=180)
    phone = serializers.CharField(max_length=40, required=False, allow_blank=True)
    country = serializers.CharField(max_length=120, required=False, allow_blank=True)
    city = serializers.CharField(max_length=120, required=False, allow_blank=True)
    postcode = serializers.CharField(max_length=20, required=False, allow_blank=True)
    latitude = serializers.DecimalField(
        max_digits=9, decimal_places=6, required=False, allow_null=True
    )
    longitude = serializers.DecimalField(
        max_digits=9, decimal_places=6, required=False, allow_null=True
    )
    favourite_cuisines = serializers.ListField(
        child=serializers.CharField(max_length=80), required=False
    )
    dietary_preferences = serializers.ListField(
        child=serializers.CharField(max_length=80), required=False
    )
    allergens_to_avoid = serializers.ListField(
        child=serializers.CharField(max_length=80), required=False
    )
    max_delivery_time = serializers.IntegerField(required=False, allow_null=True)
    preferred_price_level = serializers.IntegerField(
        min_value=1, max_value=4, required=False, allow_null=True
    )

    def validate_email(self, value):
        email = UserModel.objects.normalize_email(value)
        if UserModel.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Unable to register with these details.")
        return email

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        profile_fields = {
            key: validated_data.pop(key)
            for key in list(validated_data.keys())
            if key
            in {
                "country",
                "city",
                "postcode",
                "latitude",
                "longitude",
                "favourite_cuisines",
                "dietary_preferences",
                "allergens_to_avoid",
                "max_delivery_time",
                "preferred_price_level",
            }
        }
        password = validated_data.pop("password")
        user = UserModel.objects.create_user(
            password=password,
            role=User.Role.CUSTOMER,
            **validated_data,
        )
        CustomerProfile.objects.create(user=user, **profile_fields)
        create_email_verification_code(
            user,
            EmailVerificationCode.Purpose.REGISTRATION,
            enforce_cooldown=False,
        )
        return user


class OwnerRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    full_name = serializers.CharField(max_length=180)
    phone = serializers.CharField(max_length=40, required=False, allow_blank=True)
    business_name = serializers.CharField(max_length=180)
    contact_phone = serializers.CharField(max_length=40, required=False, allow_blank=True)
    business_email = serializers.EmailField()

    def validate_email(self, value):
        email = UserModel.objects.normalize_email(value)
        if UserModel.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Unable to register with these details.")
        return email

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        profile_fields = {
            "business_name": validated_data.pop("business_name"),
            "contact_phone": validated_data.pop("contact_phone", ""),
            "business_email": validated_data.pop("business_email"),
        }
        password = validated_data.pop("password")
        user = UserModel.objects.create_user(
            password=password,
            role=User.Role.RESTAURANT_OWNER,
            **validated_data,
        )
        RestaurantOwnerProfile.objects.create(user=user, **profile_fields)
        create_email_verification_code(
            user,
            EmailVerificationCode.Purpose.REGISTRATION,
            enforce_cooldown=False,
        )
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.RegexField(regex=r"^\d{6}$", write_only=True)

    def save(self, **kwargs):
        request = self.context.get("request")
        try:
            user = UserModel.objects.get(email__iexact=self.validated_data["email"])
            verify_email_code(
                user,
                self.validated_data["code"],
                EmailVerificationCode.Purpose.REGISTRATION,
            )
        except (UserModel.DoesNotExist, VerificationError):
            user = locals().get("user")
            audit_log(
                user if isinstance(user, UserModel) else None,
                SecurityAuditLog.EventType.VERIFICATION_FAILURE,
                request,
            )
            raise serializers.ValidationError({"detail": "Invalid or expired code."})

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])
        audit_log(user, SecurityAuditLog.EventType.VERIFICATION_SUCCESS, request)
        return user


class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        try:
            user = UserModel.objects.get(email__iexact=self.validated_data["email"])
            if not user.is_email_verified:
                create_email_verification_code(
                    user,
                    EmailVerificationCode.Purpose.REGISTRATION,
                    enforce_cooldown=True,
                )
        except CooldownError:
            raise serializers.ValidationError(
                {"detail": "Please wait before requesting another code."}
            )
        except UserModel.DoesNotExist:
            pass


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        request = self.context.get("request")
        email = UserModel.objects.normalize_email(attrs["email"])
        generic_error = serializers.ValidationError(
            {"detail": "Unable to log in with these credentials."}
        )

        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            audit_log(None, SecurityAuditLog.EventType.LOGIN_FAILED, request)
            raise generic_error

        if user.is_locked:
            audit_log(user, SecurityAuditLog.EventType.LOGIN_FAILED, request)
            raise generic_error

        if not user.is_email_verified:
            audit_log(user, SecurityAuditLog.EventType.LOGIN_FAILED, request)
            raise serializers.ValidationError(
                {"detail": "Please verify your email before logging in."}
            )

        authenticated_user = authenticate(
            request=request,
            username=email,
            password=attrs["password"],
        )
        if not authenticated_user:
            user.record_failed_login()
            audit_log(user, SecurityAuditLog.EventType.LOGIN_FAILED, request)
            raise generic_error

        user.reset_login_failures()
        audit_log(user, SecurityAuditLog.EventType.LOGIN_SUCCESS, request)
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": ProfileSerializer(user).data,
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data["refresh"]).blacklist()
        except Exception as exc:
            raise serializers.ValidationError({"detail": "Invalid token."}) from exc


class ProfileSerializer(serializers.ModelSerializer):
    customer_profile = serializers.SerializerMethodField()
    owner_profile = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = (
            "id",
            "email",
            "full_name",
            "role",
            "phone",
            "is_email_verified",
            "is_phone_verified",
            "date_joined",
            "customer_profile",
            "owner_profile",
        )
        read_only_fields = fields

    def get_customer_profile(self, obj):
        profile = getattr(obj, "customer_profile", None)
        if not profile:
            return None
        return CustomerProfileSerializer(profile).data

    def get_owner_profile(self, obj):
        profile = getattr(obj, "owner_profile", None)
        if not profile:
            return None
        return RestaurantOwnerProfileSerializer(profile).data


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        exclude = ("user",)


class RestaurantOwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOwnerProfile
        exclude = ("user",)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        request = self.context.get("request")
        try:
            user = UserModel.objects.get(email__iexact=self.validated_data["email"])
            create_password_reset_code(user, enforce_cooldown=True)
            audit_log(
                user,
                SecurityAuditLog.EventType.PASSWORD_RESET_REQUEST,
                request,
            )
        except CooldownError:
            raise serializers.ValidationError(
                {"detail": "Please wait before requesting another code."}
            )
        except UserModel.DoesNotExist:
            audit_log(
                None,
                SecurityAuditLog.EventType.PASSWORD_RESET_REQUEST,
                request,
            )


class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.RegexField(regex=r"^\d{6}$", write_only=True)

    def save(self, **kwargs):
        try:
            user = UserModel.objects.get(email__iexact=self.validated_data["email"])
            verify_password_reset_code(user, self.validated_data["code"], consume=False)
        except (UserModel.DoesNotExist, VerificationError):
            raise serializers.ValidationError({"detail": "Invalid or expired code."})


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.RegexField(regex=r"^\d{6}$", write_only=True)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def save(self, **kwargs):
        request = self.context.get("request")
        try:
            user = UserModel.objects.get(email__iexact=self.validated_data["email"])
            verify_password_reset_code(
                user,
                self.validated_data["code"],
                consume=True,
            )
        except (UserModel.DoesNotExist, VerificationError):
            raise serializers.ValidationError({"detail": "Invalid or expired code."})

        user.set_password(self.validated_data["new_password"])
        user.failed_login_attempts = 0
        user.locked_until = None
        user.save(update_fields=["password", "failed_login_attempts", "locked_until"])
        audit_log(user, SecurityAuditLog.EventType.PASSWORD_RESET_SUCCESS, request)
        return user
