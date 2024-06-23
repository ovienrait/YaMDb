"""Модуль регистрации моделей приложения и полей в админке."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

OBJECTS_PER_PAGE = 10

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role',)}),
)


class UsersAdmin(UserAdmin):
    """Класс настройки отображения раздела пользователей."""

    list_display = ('id', 'username', 'email', 'role', 'bio', 'first_name',
                    'last_name', 'password', 'is_superuser', 'is_staff',)
    ordering = ('username',)
    list_per_page = OBJECTS_PER_PAGE
    search_fields = ('username', 'role', 'email', 'is_staff',)
    list_editable = ('username', 'email', 'role', 'bio', 'first_name',
                     'last_name', 'password', 'is_superuser', 'is_staff',)
    list_display_links = ('id',)
    empty_value_display = 'Не задано'


admin.site.register(CustomUser, UsersAdmin)
