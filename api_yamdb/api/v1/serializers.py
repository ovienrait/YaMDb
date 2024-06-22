from rest_framework import serializers

from users.models import ROLE_CHOICES, CustomUser
from reviews.models import Genre, Category, Title


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
    genre = GenreSerializer(many=True, required=False)
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

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Название произведения не может быть '
                'длиннее 256 символов.')
        return value


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
