"""Модуль сериализатора приложения Users."""
from rest_framework import serializers

from .models import ROLE_CHOICES, CustomUser


class UserSignUpSerializer(serializers.ModelSerializer):
    """Класс сериализатора для регистрации пользователя."""

    class Meta:
        """Внутренний класс сериализатора."""

        model = CustomUser
        fields = ('username', 'email',)


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора для пользователя."""

    role = serializers.ChoiceField(
        choices=ROLE_CHOICES, required=False, read_only=True
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=False,
    )

    class Meta:
        """Внутренний класс сериализатора."""

        model = CustomUser
        fields = ('username', 'email', 'password',
                  'first_name', 'last_name', 'bio', 'role',)


class AdminSerializer(serializers.ModelSerializer):
    """Класс сериализатора для админа."""

    role = serializers.ChoiceField(
        choices=ROLE_CHOICES, required=False,
    )
    is_staff = serializers.BooleanField(
        required=False,
        write_only=True,
        )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=False,
    )

    class Meta:
        """Внутренний класс сериализатора."""

        model = CustomUser
        fields = ('username', 'email', 'is_staff', 'password',
                  'first_name', 'last_name', 'bio', 'role',)
