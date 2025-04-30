from rest_framework.permissions import BasePermission
class IsCitoyen(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'citoyen'
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

