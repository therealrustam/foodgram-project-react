from rest_framework import permissions


class AllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
