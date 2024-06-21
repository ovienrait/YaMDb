from rest_framework import viewsets

from reviews.models import Genre, Category, Title
from .serializers import (
    GenreSerializer, CategorySerializer, TitleGETSerializer, TitleSerializer)
from .mixins import ListCreateDestroyViewSet


class GenreViewSet(ListCreateDestroyViewSet):
    """Обработчик объектов модели жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """Обработчик объектов модели категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Обработчик объектов модели произведений"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer
