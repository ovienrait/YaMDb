"""Модуль моделей приложения."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser


class BaseModel(models.Model):
    """Абстрактная модель для жанров и категорий."""

    name = models.CharField(
        max_length=256, verbose_name='название')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        """Метод возвращающий имя."""
        return self.name


class Genre(BaseModel):
    """Модель для жанров."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(BaseModel):
    """Модель для категорий."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель для произведений."""

    genre = models.ManyToManyField(
        Genre, through='TitleGenre', verbose_name='жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='категория')
    name = models.TextField(max_length=256, verbose_name='название')
    year = models.IntegerField(verbose_name='год выпуска')
    description = models.TextField(
        verbose_name='описание', null=True, blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        """Метод возвращающий имя произведения."""
        return self.name


class TitleGenre(models.Model):
    """Модель для связи произведений и жанров."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='название')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='жанр')

    class Meta:
        verbose_name = 'произведение/жанр'
        verbose_name_plural = 'Произведение/Жанр'


class Review(models.Model):
    """Класс отзывов."""

    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Aвтор')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='произведение', null=True
    )
    text = models.TextField(verbose_name='текст')
    score = models.PositiveIntegerField(
        verbose_name='Oценка',
        validators=[
            MinValueValidator(1, message='Введенная оценка ниже допустимой'),
            MaxValueValidator(10, message='Введенная оценка выше допустимой')]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        default_related_name = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        """Метод возвращающий текст ревью."""
        return self.text[:50]


class Comment(models.Model):
    """Класс комментариев."""

    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Aвтор')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='oтзыв')
    text = models.TextField(verbose_name='текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
        default_related_name = 'comments'

    def __str__(self):
        """Метод возвращающий текст комментария."""
        return self.text[:50]
