from django.contrib import admin

from .models import Genre, Category, Title, TitleGenre

OBJECTS_PER_PAGE = 10


class GenreAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела жанров"""
    list_display = ('name', 'slug')
    ordering = ('name',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела категорий"""
    list_display = ('name', 'slug')
    ordering = ('name',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела произведений"""
    list_display = (
        'name', 'year', 'description', 'get_genre', 'category')
    empty_value_display = 'не указано'
    ordering = ('name',)
    search_fields = ('name', 'year')

    def get_genre(self, object):
        return ',\n'.join((genre.name for genre in object.genre.all()))

    get_genre.short_description = 'жанр'


class TitleGenreAdmin(admin.ModelAdmin):
    """Класс настройки отображения раздела отношений
    произведений к жанрам"""
    list_display = ('title', 'genre')
    ordering = ('title',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('title', 'genre')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(TitleGenre, TitleGenreAdmin)
