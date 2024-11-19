from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """
    If user is owner
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
