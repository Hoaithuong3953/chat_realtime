from rest_framework.permissions import BasePermission

from apps.accounts.enums import Role

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == Role.ADMIN
        )