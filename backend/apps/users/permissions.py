from rest_framework.permissions import BasePermission

from .models import User


class HasRole(BasePermission):
    allowed_roles: set[str] = set()

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_email_verified
            and request.user.role in self.allowed_roles
        )


class IsCustomer(HasRole):
    allowed_roles = {User.Role.CUSTOMER, User.Role.SUPER_ADMIN}


class IsRestaurantOwner(HasRole):
    allowed_roles = {User.Role.RESTAURANT_OWNER, User.Role.SUPER_ADMIN}


class IsAdminRole(HasRole):
    allowed_roles = {User.Role.ADMIN, User.Role.SUPER_ADMIN}


class IsSuperAdmin(HasRole):
    allowed_roles = {User.Role.SUPER_ADMIN}


class IsVerifiedUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_email_verified
        )
