from rest_framework import serializers

from api.models import Word


class WordSerializer(serializers.ModelSerializer):
    """Сериализатор для модели слов."""

    class Meta:
        model = Word
        fields = ['word']


class WordListSerializer(serializers.Serializer):
    """Сериализатор для ответа пользователю на его запрос."""

    language = serializers.CharField(max_length=3)
    quantity = serializers.IntegerField()
    words = serializers.ListField(child=serializers.CharField())
