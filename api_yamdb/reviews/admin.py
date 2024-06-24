"""Модуль настройки админки."""
from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, TitleGenre

OBJECTS_PER_PAGE = 10


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела жанров."""

    list_display = ('name', 'slug')
    list_display_links = ('name',)
    ordering = ('name',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела категорий."""

    list_display = ('name', 'slug')
    list_display_links = ('name',)
    ordering = ('name',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела произведений."""

    list_display = (
        'name', 'year', 'description', 'get_genre', 'category')
    list_display_links = ('name',)
    empty_value_display = 'не указано'
    ordering = ('name',)
    search_fields = ('name', 'year')

    @admin.display(description='жанр')
    def get_genre(self, object):
        """Метод получения жанра."""
        return ',\n'.join((genre.name for genre in object.genre.all()))


@admin.register(TitleGenre)
class TitleGenreAdmin(admin.ModelAdmin):
    """
    Класс TitleGenreAdmin.

    Для настройки отображения раздела отношений произведений к жанрам.
    """

    list_display = ('title', 'genre')
    list_display_links = ('title',)
    ordering = ('title',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('title', 'genre')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки раздела отзывов."""

    list_display = (
        'pk', 'author', 'short_text', 'score', 'pub_date', 'title')
    list_display_links = ('short_text',)
    list_filter = ('author', 'score', 'pub_date')
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('author',)

    @admin.display(description='текст')
    def short_text(self, obj):
        return obj.text[:50]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""

    list_display = (
        'pk', 'author', 'short_text', 'pub_date', 'review')
    list_display_links = ('short_text',)
    list_filter = ('author', 'pub_date')
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('author',)

    @admin.display(description='текст')
    def short_text(self, obj):
        return obj.text[:50]
