"""Модуль пользовательских разрешений."""
from rest_framework import permissions

from users.models import CustomUser


class IsAdminOnly(permissions.BasePermission):
    """Класс пользовательского разрешения."""

    def has_permission(self, request, view):
        """
        Метод проверки.

        Является ли пользователь админом или суперпользователем.
        """
        return request.user.is_authenticated and (
            CustomUser.objects.get(id=request.user.id).role == 'admin' or (
                CustomUser.objects.get(id=request.user.id).is_superuser == 1)
        )


class IsModerator(permissions.BasePermission):
    """Класс пользовательского разрешения."""

    def has_permission(self, request, view):
        """Метод проверки является ли пользователь модератором."""
        return request.user.is_authenticated and (
            CustomUser.objects.get(id=request.user.id).role == 'moderator'
        )
