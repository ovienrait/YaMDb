"""Модуль класса приложения Reviews."""
from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Класс приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
