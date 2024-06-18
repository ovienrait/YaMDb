from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, CategoryViewSet, TitleViewSet

router = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
