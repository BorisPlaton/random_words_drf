from rest_framework import serializers

from api.models import Word


class WordSerializer(serializers.ModelSerializer):
    """Сериализатор для модели слов."""

    class Meta:
        model = Word
        fields = ['word', 'language']
