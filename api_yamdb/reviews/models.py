from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    """Модель для жанров"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Category(models.Model):
    """Модель для категорий"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель для произведений"""
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField(null=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель для связи произведений и жанров"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
