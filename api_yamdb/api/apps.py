"""Модуль класса приложения v1."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Класс приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
