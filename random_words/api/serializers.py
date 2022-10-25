from rest_framework import serializers

from api.models import Word


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
    quantity = serializers.IntegerField()
    words = WordSerializer(many=True)
