from typing import TypedDict

from django.db.models import QuerySet

from api.models import Word, WordsLanguage
from api.selectors import get_random_words


class UserResponse(TypedDict):
    """
    The response that will be sent to the user as an answer
    on his request.
    """
    language: str
    quantity: int
    words: QuerySet[Word]


def get_words_user_response_dict(words_amount: int, language: str) -> UserResponse:
    """
    Retrieves words from the database and constructs a dictionary
    with all necessary data.
    """
    words = get_random_words(words_amount, language)
    return UserResponse(language=language, quantity=words_amount, words=words)


def load_new_words(words: list[str], words_language: str) -> int:
    """
    Inserts many words with a specific language to the database.
    Returns new created records.
    """
    validate_words_language(words_language)
    return Word.objects.bulk_create(
        [Word(word=word, language=words_language) for word in words]
    )


def validate_words_language(words_language: str):
    """
    Checks if words language is registered for models. If not,
    raises an exception.
    """
    if words_language not in WordsLanguage.values:
        raise ValueError("`%s` isn't a correct words language." % words_language)
