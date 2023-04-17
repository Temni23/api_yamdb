from rest_framework import permissions


class IsAuthorStaffOrReadOnly(permissions.BasePermission):
    '''Разрешение дает доступ для редактирования автору, администратору
        или модератору, для остальных только чтение'''

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author == request.user or
                request.user.is_admin or
                request.user.is_moderator or request.user.is_superuser)


class IsAdminOrSuperuserOrReadOnly(permissions.BasePermission):
    '''Разрешение дает доступ для редактирования администратору,
       для остальных только чтение'''

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated and
                (request.user.is_admin or request.user.is_superuser))


class IsAdminOrSuperuser(permissions.BasePermission):
    '''Разрешение дает доступ администратору и суперюзеру'''

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or
                                                  request.user.is_superuser)
