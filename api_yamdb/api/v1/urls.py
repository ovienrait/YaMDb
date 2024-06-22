from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AdminCreateList, AdminDetail, UserObtainTokenAPI, UserRetrieveUpdateAPI,
    UserSignupAPI, GenreViewSet, CategoryViewSet, TitleViewSet,
    ReviewViewSet, CommentViewSet)

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
    path('auth/signup/', UserSignupAPI.as_view()),
    path('auth/token/', UserObtainTokenAPI.as_view()),
    path('users/me/', UserRetrieveUpdateAPI.as_view()),
    path('users/', AdminCreateList.as_view()),
    path('users/<username>/', AdminDetail.as_view()),
    path('', include(router.urls)),
]
