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


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс пользовательского разрешения."""

    def has_permission(self, request, view):
        if request.user.id:
            return CustomUser.objects.get(
                id=request.user.id).role == 'admin' or (
                CustomUser.objects.get(id=request.user.id).is_superuser == 1)
        else:
            return request.method in permissions.SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс пользовательского разрешения"""

    def has_object_permission(self, request, view, obj):
        """Метод проверки является ли пользователь автором."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user or (
                request.user.role == 'moderator' or (
                    request.user.role == 'admin')))
