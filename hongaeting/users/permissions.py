from rest_framework import permissions


class IsSameUserWithRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, views, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
