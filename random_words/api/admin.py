from django.contrib import admin

from api.models import Word


@admin.register(Word)
class WordsAdmin(admin.ModelAdmin):
    """Админ панель для модели слов."""

    list_display = ['word', 'language']
    list_filter = ['language']
