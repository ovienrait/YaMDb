from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AdminCreateList, AdminDetail, UserObtainTokenAPI, UserRetrieveUpdateAPI,
    UserSignupAPI, GenreViewSet, CategoryViewSet, TitleViewSet)

router = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('auth/signup/', UserSignupAPI.as_view()),
    path('auth/token/', UserObtainTokenAPI.as_view()),
    path('users/me/', UserRetrieveUpdateAPI.as_view()),
    path('users/', AdminCreateList.as_view()),
    path('users/<username>/', AdminDetail.as_view()),
    path('', include(router.urls)),
]
