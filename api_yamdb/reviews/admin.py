"""Модуль настройки админки."""
from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, TitleGenre

OBJECTS_PER_PAGE = 10


class GenreAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела жанров."""

    list_display = ('name', 'slug')
    ordering = ('name',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела категорий."""

    list_display = ('name', 'slug')
    ordering = ('name',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела произведений."""

    list_display = (
        'name', 'year', 'description', 'get_genre', 'category')
    empty_value_display = 'не указано'
    ordering = ('name',)
    search_fields = ('name', 'year')

    @admin.display(description='жанр')
    def get_genre(self, object):
        """Метод получения жанра."""
        return ',\n'.join((genre.name for genre in object.genre.all()))


class TitleGenreAdmin(admin.ModelAdmin):
    """
    Класс TitleGenreAdmin.

    Для настройки отображения раздела отношений произведений к жанрам.
    """

    list_display = ('title', 'genre')
    ordering = ('title',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('title', 'genre')


class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки раздела отзывов."""

    list_display = (
        'pk', 'author', 'text', 'score', 'pub_date', 'title')
    list_filter = ('author', 'score', 'pub_date')
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('author',)


class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""

    list_display = (
        'pk', 'author', 'text', 'pub_date', 'review')
    list_filter = ('author', 'pub_date')
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('author',)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(TitleGenre, TitleGenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
