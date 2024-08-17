from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает редактирование только владельцу объекта.
    Просмотр доступен всем авторизованным пользователям.
    """
    def has_object_permission(self, request, view, obj):
        # Доступ на чтение (GET, HEAD, OPTIONS) разрешен всем авторизованным пользователям
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Редактировать профиль может только владелец
        return obj == request.user
