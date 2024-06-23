"""Модуль кастомных миксинов."""
from rest_framework import mixins, viewsets
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAdminOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для получения списка объектов.

    Создания нового объекта, удаления существующего объекта.
    """

    pass


class DeleteBySlugMixin:
    """Кастомный миксин для DELETE-запросов по полю slug"""

    @action(
        detail=False, methods=['delete'],
        url_path='(?P<slug>[^/.]+)',
        permission_classes=(IsAdminOnly,))
    def delete_by_slug(self, request, slug=None):
        model = self.get_queryset().model
        obj = get_object_or_404(model, slug=slug)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
