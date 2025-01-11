from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Custom permission for Managers to perform all CRUD operations.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'


class IsTechnician(permissions.BasePermission):
    """
    Custom permission for Technicians to perform CRU operations (no delete).
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'technician':
            return request.method in ['GET', 'PUT', 'PATCH']
        return False


class IsClient(permissions.BasePermission):
    """
    Custom permission for Clients to view tasks only (read-only access).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client'

    def has_object_permission(self, request, view, obj):
        return request.method == 'GET'
