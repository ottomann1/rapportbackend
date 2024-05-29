from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="superadmin").exists()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="admin").exists()


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="user").exists()


class IsCompanyAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return (
            obj.company == request.user.profile.company
            and request.user.groups.filter(name="admin").exists()
        )


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return obj.submitted_by == request.user
