from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_superuser
