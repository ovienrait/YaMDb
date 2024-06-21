import re
from rest_framework import serializers
from django.core.validators import MaxLengthValidator

from reviews.models import Genre, Category, Title
from users.models import User, roles
from .validators import username_validator, unique_username_validator


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    def validate_username(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                "Username must be 150 characters or less.")
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError("Invalid username format.")
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                "Email must be 254 characters or less.")
        return value


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора для пользователя."""

    role = serializers.ChoiceField(
        choices=roles, required=False, read_only=True
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=False,
    )
    username = serializers.CharField(
        validators=[username_validator, MaxLengthValidator(150),
                    unique_username_validator],
    )

    class Meta:
        """Внутренний класс сериализатора."""

        model = User
        fields = ('username', 'email', 'password',
                  'first_name', 'last_name', 'bio', 'role',)


class AdminSerializer(serializers.ModelSerializer):
    """Класс сериализатора для админа."""

    role = serializers.ChoiceField(
        choices=roles, required=False,
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
    username = serializers.CharField(
        validators=[username_validator, MaxLengthValidator(150),
                    unique_username_validator],
    )

    class Meta:
        """Внутренний класс сериализатора."""

        model = User
        fields = ('username', 'email', 'is_staff', 'password',
                  'first_name', 'last_name', 'bio', 'role',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категорий"""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведений при GET-запросе"""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        read_only_fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведений при небезопасном запросе"""
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        many=True, required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
