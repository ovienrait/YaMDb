"""Модуль кастомных миксинов."""
from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для получения списка объектов.

    Создания нового объекта, удаления существующего объекта.
    """

    pass
