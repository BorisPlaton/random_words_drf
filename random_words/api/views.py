from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import WordListSerializer
from api.services import get_words_user_response, validate_words_language


class WordsViewSet(mixins.ListModelMixin, GenericViewSet):
    """The `ViewSet` for retrieving words records."""

    serializer_class = WordListSerializer

    def list(self, request, *args, **kwargs):
        """Returns a JSON with words."""
        data = get_words_user_response(self.get_words_amount(), self.get_words_language())
        return Response(self.get_serializer(data).data, status=204 if not data.words else 200)

    def get_words_language(self) -> str:
        """
        Returns words' language that user has specified in query
        parameters. If none, returns Russian.
        """
        if (words_language := self.request.query_params.get('language')) is None:
            return 'ru'
        validate_words_language(words_language)
        return words_language

    def get_words_amount(self) -> int:
        """
        Returns words amount that user has specified. If none,
        returns 200.
        """
        if (words_amount := self.request.query_params.get('quantity')) is None:
            return 200
        try:
            words_amount = int(words_amount)
        except ValueError:
            raise ValueError("Количество слов должно быть числом, а не `%s`" % words_amount)
        if words_amount < 0:
            raise ValueError("Количество слов не может быть меньше нуля.")
        return words_amount
