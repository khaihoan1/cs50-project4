from rest_framework import permissions


class JustOwnerCanModifyComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return request.user == obj.owner
        return True
