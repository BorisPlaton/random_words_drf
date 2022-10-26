import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.response import Response

from api.models import Word


@pytest.mark.django_db
class TestViews:

    def test_view_returns_response_with_204_status_code(self, client):
        res: Response = client.get(reverse('words-list'))
        assert res.status_code == 204
        assert res.data['language'] == 'ru'
        assert res.data['quantity'] == 0
        assert res.data['words'] == []

    @pytest.mark.parametrize(
        'language',
        ['ru', 'ua', 'eng']
    )
    def test_view_returns_response_with_user_specified_language(self, client, language):
        res: Response = client.get(reverse('words-list') + f'?language={language}')
        assert res.status_code == 204
        assert res.data['language'] == language

    @pytest.mark.parametrize(
        'language',
        ['en', 'du', 'pol', 'a']
    )
    def test_view_returns_response_with_invalid_language(self, client, language):
        res: Response = client.get(reverse('words-list') + f'?language={language}')
        assert res.status_code == 400
        assert res.data['details']

    @pytest.mark.parametrize(
        'quantity',
        [1, 5, 10]
    )
    def test_view_returns_response_with_zero_words_quantity_if_none_words_present(self, client, quantity):
        res: Response = client.get(reverse('words-list') + f'?quantity={quantity}')
        assert res.status_code == 204
        assert res.data['quantity'] == 0

    @pytest.mark.parametrize(
        'quantity',
        ['2a', 'sss', -20]
    )
    def test_400_status_code_if_invalid_words_quantity(self, client, quantity):
        res: Response = client.get(reverse('words-list') + f'?quantity={quantity}')
        assert res.status_code == 400
        assert res.data['details']

    def test_all_words_returned_if_amount_bigger_than_words_quantity(self, client):
        baker.make(Word, language='ru', _quantity=5)
        res = client.get(reverse('words-list') + '?quantity=100')
        assert res.data['quantity'] == 5
        assert len(res.data['words']) == 5

    def test_response_returns_list_with_strings(self, client):
        baker.make(Word, language='ru', _quantity=5)
        res = client.get(reverse('words-list') + '?quantity=100')
        for word in res.data['words']:
            assert isinstance(word, str)
