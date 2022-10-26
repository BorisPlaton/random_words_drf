from unittest.mock import patch, MagicMock

import pytest

from api.models import Word
from api.services import get_words_user_response, UserWordsResponse, validate_words_language, load_new_words


@patch('api.services.get_random_words')
def test_get_words_response_returned_value(get_words_mock: MagicMock):
    language = 'ru'
    words = []
    get_words_mock.side_effect = lambda x, y: []
    words_dict = get_words_user_response(10, language)
    assert isinstance(words_dict, UserWordsResponse)
    assert words_dict.language == language
    assert words_dict.words == words


@pytest.mark.django_db
def test_user_words_response_dataclass_is_subscriptable():
    language = 'eng'
    words = Word.objects.all()
    words_response = UserWordsResponse(language, words)
    assert words_response['language'] == language
    assert words_response['words'] == words


@pytest.mark.parametrize(
    'words_language',
    ['ru', 'eng', 'ua']
)
def test_validation_of_words_language_is_passed_if_languages_are_registered(words_language):
    assert validate_words_language(words_language) is None


@pytest.mark.parametrize(
    'words_language',
    ['ru_', 'eng1', 'ua2', '', 's']
)
def test_validation_of_words_language_raises_exception_if_language_is_wrong(words_language):
    with pytest.raises(ValueError):
        validate_words_language(words_language)


@pytest.mark.django_db
def test_all_words_are_loaded_to_db():
    words = ['1', '2', 'word', 'another_word']
    language = 'eng'
    load_new_words(words, language)
    for word in words:
        assert Word.objects.get(word=word)
