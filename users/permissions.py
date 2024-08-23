from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Moderators').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='moderator').exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


#
#
# class IsOwnerOrReadOnly(BasePermission):
#     """
#     Разрешает редактирование только владельцу объекта.
#     Просмотр доступен всем авторизованным пользователям.
#     """
#     def has_object_permission(self, request, view, obj):
#         # Доступ на чтение (GET, HEAD, OPTIONS) разрешен всем авторизованным пользователям
#         if request.method in ['GET', 'HEAD', 'OPTIONS']:
#             return True
#         # Редактировать профиль может только владелец
#         return obj == request.user
#
#
# class IsModeratorOrOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Доступ разрешен, если пользователь является модератором или владельцем объекта
#         return request.user and (
#                 request.user.groups.filter(name='Moderators').exists() or obj.owner == request.user
#         )
#
#     def has_permission(self, request, view):
#         # Доступ разрешен для всех аутентифицированных пользователей на 'list' и 'retrieve'
#         if request.method in ['GET', 'HEAD', 'OPTIONS']:
#             return True
#         return request.user and request.user.is_authenticated
#
