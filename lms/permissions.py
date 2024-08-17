from rest_framework.permissions import BasePermission
from rest_framework import permissions


from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Moderators').exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModeratorOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Доступ разрешен, если пользователь является модератором или владельцем объекта
        return request.user and (
                request.user.groups.filter(name='Moderators').exists() or obj.owner == request.user
        )

    def has_permission(self, request, view):
        # Доступ разрешен для всех аутентифицированных пользователей на 'list' и 'retrieve'
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_authenticated



# class IsModerator(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='Moderators').exists()
#
#
# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Разрешить доступ только владельцам объектов или модераторам.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Разрешить просмотр и получение данных любому авторизованному пользователю
#         if request.method in permissions.SAFE_METHODS:
#             return False
#
#         # Разрешить изменение и удаление объекта только владельцу или модератору
#         if request.user.groups.filter(name='Moderators').exists():
#             return True
#
#         return obj.owner == request.user


# class IsModerator(BasePermission):
#     """
#     Разрешает доступ только модераторам.
#     """
#
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.groups.filter(name='Moderators').exists()
#
#     def has_object_permission(self, request, view, obj):
#         # Разрешить только чтение и редактирование, запретить удаление и создание
#         if request.method in ['GET', 'PUT', 'PATCH']:
#             return True
#         return False


# class IsModeratorOrOwner(permissions.BasePermission):
#     """
#     Разрешить доступ только владельцам объекта или модераторам.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Разрешить доступ на чтение всем пользователям
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         # Если пользователь модератор, разрешить все действия
#         if request.user.groups.filter(name='Moderators').exists():
#             return True
#
#         # Разрешить изменение только владельцу объекта
#         return obj.owner == request.user
