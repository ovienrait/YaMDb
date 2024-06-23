"""Модуль класса приложения Users."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Класс приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'
