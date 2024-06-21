from django.core.validators import RegexValidator
from rest_framework import serializers

from users.models import User

username_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Username может содержать буквы, цифры и '
    'следующие символы: @/./+/-/_',
)


def unique_username_validator(value):
    """Пользователь с таким username уже существует."""
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError(
            'Пользователь с таким username уже существует.')
