from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Вьюсет для получения списка объектов,
    создания нового объекта, удаления существующего объекта"""
    pass
