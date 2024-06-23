"""Модуль маршрутизатора приложения."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdminCreateList, AdminDetail, CategoryViewSet,
                    CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
                    UserObtainTokenAPI, UserRetrieveUpdateAPI, UserSignupAPI)

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('auth/signup/', UserSignupAPI.as_view(), name='signup'),
    path('auth/token/', UserObtainTokenAPI.as_view(), name='obtain_token'),
    path('users/me/', UserRetrieveUpdateAPI.as_view(), name='update_user'),
    path('users/', AdminCreateList.as_view(), name='admin_create_user_list'),
    path('users/<username>/', AdminDetail.as_view(), name='user_detail'),
    path('', include(router.urls)),
]
