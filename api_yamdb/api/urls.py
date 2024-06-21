from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (GenreViewSet, CategoryViewSet, TitleViewSet,
                    SignUpView, TokenObtainView, UserRetrieveUpdateAPI,
                    AdminCreateList, AdminDetail)

router = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
    path('v1/users/me/', UserRetrieveUpdateAPI.as_view()),
    path('v1/users/', AdminCreateList.as_view()),
    path('v1/users/<str:username>/', AdminDetail.as_view()),
    path('v1/', include(router.urls)),
]
