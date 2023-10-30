from rest_framework.permissions import BasePermission


class PermissionAll(BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        return True
