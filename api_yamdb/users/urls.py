"""Модуль маршрутизатора приложения Users."""
from django.urls import path

from .views import (AdminCreateList, AdminDetail,
                    UserObtainTokenAPI, UserRetrieveUpdateAPI, UserSignupAPI)

urlpatterns = [
    path('auth/signup/', UserSignupAPI.as_view()),
    path('auth/token/', UserObtainTokenAPI.as_view()),
    path('users/me/', UserRetrieveUpdateAPI.as_view()),
    path('users/', AdminCreateList.as_view()),
    path('users/<username>/', AdminDetail.as_view())
]
