from django.contrib import admin

from api.models import Word


@admin.register(Word)
class WordsAdmin(admin.ModelAdmin):
    """Админ панель для модели слов."""

    list_display = ['id', 'word', 'language']
    ordering = ['id']
    list_filter = ['language']
