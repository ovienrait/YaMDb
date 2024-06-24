"""Модуль модели приложения Users."""
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class CustomUser(AbstractUser):
    """Пользовательская модель приложения."""

    email = models.EmailField(max_length=254, unique=True, blank=False)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', max_length=16, choices=ROLE_CHOICES, default='user'
    )
    REQUIRED_FIELDS = ('email',)

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Метод возвращающий имя пользователя."""
        return self.username
