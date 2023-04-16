from rest_framework import permissions


class IsAuthorStaffOrReadOnly(permissions.BasePermission):
    """Разрешение дает доступ для редактирования автору, администратору
        или модератору, для остальных только чтение"""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author == request.user or
                request.user.is_admin or
                request.user.is_moderator)


class IsAdmin(permissions.BasePermission):
    """Разрешение дает доступ администратору"""

    def has_permission(self, request, view):
        return request.user.is_admin
