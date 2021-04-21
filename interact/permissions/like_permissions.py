from rest_framework import permissions


class JustNotOwnerCanLike(permissions.BasePermission):
    def has_object_permission(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user != obj.owner
