import random

from django.db.models import QuerySet

from api.models import Word


def get_random_words(words_amount: int, language: str) -> QuerySet[Word]:
    """
    Return the `QuerySet` of `Word` records. You have to specify
    a length of sequence and a words' language.
    """
    words = get_words_of_language(language)
    try:
        id_list = random.sample(list(words.values_list('id', flat=True)), words_amount)
    except ValueError:
        return words
    return words.filter(id__in=id_list)


def get_words_of_language(words_language: str) -> QuerySet[Word]:
    """Returns words of a specific language."""
    words = Word.objects.filter(language=words_language)
    return words
