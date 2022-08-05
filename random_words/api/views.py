import random

from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.exceptions import ExceptionMixin
from api.models import Word
from api.serializers import WordSerializer


class WordsViewSet(ExceptionMixin, mixins.ListModelMixin, GenericViewSet):
    """`ViewSet` для взаимодействия с моделью слов."""

    serializer_class = WordSerializer
    words_amount = 200
    allowed_words_languages = ['ru', 'eng']
    default_language = 'ru'

    def list(self, request, *args, **kwargs):
        """Возвращает список случайных слов."""
        serializer: WordSerializer = self.get_serializer(self.get_random_words(), many=True)
        return Response(serializer.data)

    def get_queryset(self) -> QuerySet:
        """
        Возвращает список слов на языке, который передается
        в параметре запроса.
        """
        return Word.objects.filter(
            language=self.request.query_params.get('language', 'ru')
        )

    def get_words_amount(self) -> int:
        """
        Возвращает значение количества слов, которое требует
        пользователь.
        """
        words_amount = self.request.query_params.get('quantity', self.words_amount)
        if words_amount is None:
            raise ValueError("Невозможно узнать количество слов, укажите параметр `quantity`.")

        try:
            words_amount = int(words_amount)
        except ValueError:
            raise ValueError("Количество слов должно быть числом, а не `%s`" % words_amount)

        if words_amount <= 0:
            raise ValueError("Количество слов не может быть меньше или равняться нулю.")
        return words_amount

    def get_words_language(self) -> str:
        """
        Возвращает язык слов, который указал пользователь
        в параметрах запроса.
        """
        words_language = self.request.query_params.get(
            'language', self.default_language
        )
        if words_language not in self.allowed_words_languages:
            raise ValueError("Недопустимый язык слов `%s`" % words_language)
        return words_language

    def get_random_words(self) -> QuerySet:
        """Возвращает список случайных слов."""
        queryset = self.get_queryset()
        random_words_id = random.sample(
            list(queryset.values_list('id', flat=True)),
            self.get_words_amount()
        )
        return queryset.filter(id__in=random_words_id)
