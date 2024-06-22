from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    """Модель для жанров"""
    name = models.CharField(
        max_length=256, verbose_name='название жанра')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для категорий"""
    name = models.CharField(
        max_length=256, verbose_name='название категории')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для произведений"""
    name = models.TextField(verbose_name='название')
    year = models.IntegerField(verbose_name='год выпуска')
    description = models.TextField(
        verbose_name='описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre, through='TitleGenre', verbose_name='жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='категория'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель для связи произведений и жанров"""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='название')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='жанр')

    class Meta:
        verbose_name = 'произведение/жанр'
        verbose_name_plural = 'Произведение/Жанр'


class Review(models.Model):
    """Класс отзывов."""
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Aвтор')
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
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение', null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )
    def __str__(self):
        return self.text


class Comment(models.Model):
    """Класс комментариев."""
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='oтзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text