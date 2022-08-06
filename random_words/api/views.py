import random
from typing import TypedDict

from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.exceptions import ExceptionMixin
from api.models import Word
from api.serializers import WordListSerializer


class UserResponse(TypedDict):
    language: str
    quantity: int
    words: QuerySet


class WordsViewSet(ExceptionMixin, mixins.ListModelMixin, GenericViewSet):
    """`ViewSet` для взаимодействия с моделью слов."""

    serializer_class = WordListSerializer
    words_amount = 200
    allowed_words_languages = ['ru', 'eng']
    default_language = 'ru'

    def list(self, request, *args, **kwargs):
        """Возвращает список случайных слов."""
        data = self.get_response_dict()
        serializer: WordListSerializer = self.get_serializer(data)
        status = 204 if not data['words'] else 200
        return Response(serializer.data, status=status)

    def get_queryset(self) -> QuerySet:
        """
        Возвращает список слов на языке, который передается
        в параметре запроса.
        """
        return Word.objects.filter(language=self.get_words_language())

    def get_response_dict(self) -> UserResponse:
        words = self.get_words_list()
        quantity = words.count()
        data: UserResponse = {
            'language': self.get_words_language(),
            'quantity': quantity,
            'words': words,
        }
        return data

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

        if words_amount < 0:
            raise ValueError("Количество слов не может быть меньше нуля.")
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
            raise ValueError("Неизвестный язык `%s`" % words_language)
        return words_language

    def get_words_list(self) -> QuerySet:
        """Возвращает список случайных слов."""
        queryset = self.get_queryset()
        words_amount = self.get_words_amount()

        if not (queryset.exists() and words_amount):
            return queryset

        id_list = list(queryset.values_list('id', flat=True))
        try:
            id_list = random.sample(id_list, words_amount)
        except ValueError:
            pass

        return queryset.filter(id__in=id_list).values_list('word', flat=True)
