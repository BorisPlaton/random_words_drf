import pytest
from model_bakery import baker

from api.models import Word
from api.selectors import get_words_of_language, get_random_words


@pytest.mark.django_db
class TestDBSelectors:

    def test_only_words_of_specific_language_are_returned(self):
        ru_words = baker.make(Word, language='ru', _quantity=10)
        eng_words = baker.make(Word, language='eng', _quantity=5)
        for ru_word in get_words_of_language('ru'):
            assert ru_word in ru_words
            assert ru_word not in eng_words

    def test_get_random_words_returns_specified_amount_of_words(self):
        baker.make(Word, language='ru', _quantity=20)
        words_quantity = 10
        all_words = get_random_words(words_quantity, 'ru')
        assert all_words.count() == words_quantity

    def test_get_random_words_returns_all_words_from_db_if_amount_too_big(self):
        total_words_quantity = 2
        baker.make(Word, language='ru', _quantity=total_words_quantity)
        all_words = get_random_words(200, 'ru')
        assert all_words.count() == total_words_quantity
