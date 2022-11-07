import random

from rest_framework import serializers

from api.models import Word
from api.services import UserWordsResponse


class WordSerializer(serializers.ModelSerializer):
    """The serializer for the `Word` model."""

    class Meta:
        model = Word
        fields = ['word']


class WordListSerializer(serializers.Serializer):
    """
    The serializer for response on user's request to get
    a words list.
    """

    language = serializers.CharField()
    quantity = serializers.SerializerMethodField()
    words = serializers.SerializerMethodField()

    def get_quantity(self, obj: UserWordsResponse) -> int:
        """Returns words amount."""
        return obj['words'].count()

    def get_words(self, obj: UserWordsResponse) -> list[str]:
        """Returns list of words and randomize them."""
        sorted_words_list = [word.word for word in obj.words.all()]
        random.shuffle(sorted_words_list)
        return sorted_words_list
