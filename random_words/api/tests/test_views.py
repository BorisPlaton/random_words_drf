from parameterized import parameterized
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.models import Word
from api.views import WordsViewSet


class TestWordsViewSet(APITestCase):
    fixtures = ['eng.json', 'ru.json']

    @parameterized.expand([
        ('ru', 50),
        ('ru', 1),
        ('ru', 5),
        ('eng', 200),
        ('eng', 10),
        ('eng', 101),
    ])
    def test_response_with_correct_query_parameters(self, language, quantity):
        url = reverse('words-list') + f'?language={language}&quantity={quantity}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response['language'], language)
        self.assertEqual(response['quantity'], quantity)
        self.assertEqual(len(response['words']), quantity)

    @parameterized.expand([
        ('eng', 409),
        ('eng', 410),
        ('eng', 500),
    ])
    def test_response_status_with_bigger_words_quantity(self, language, quantity):
        url = reverse('words-list') + f'?language={language}&quantity={quantity}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response['language'], language)
        self.assertEqual(response['quantity'], len(response['words']))
        self.assertEqual(response['quantity'], Word.objects.filter(language=language).count())

    @parameterized.expand([
        'rus',
        'engs',
        'ua',
        '2',
        (3,),
        ''
    ])
    def test_response_status_with_incorrect_language(self, language):
        url = reverse('words-list') + f'?language={language}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.content)
        self.assertEqual(response['detail'], f"Неизвестный язык `{language}`")

    @parameterized.expand([
        'rus',
        'engs',
        'ua',
        '2s',
    ])
    def test_response_status_with_incorrect_quantity(self, quantity):
        url = reverse('words-list') + f'?quantity={quantity}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.content)
        self.assertTrue(response['detail'].startswith('Количество слов должно быть числом'))

    def test_view_without_words_quantity_attribute_and_query_parameter(self):
        WordsViewSet.words_amount = None
        response = self.client.get(reverse('words-list'), format='json')
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.content)
        self.assertTrue(response['detail'].startswith("Невозможно узнать количество слов"))

    @parameterized.expand([
        '-2',
        '-1',
        '-22222',
    ])
    def test_negative_words_quantity_parameter(self, quantity):
        response = self.client.get(reverse('words-list') + f'?quantity={quantity}', format='json')
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.content)
        self.assertTrue(response['detail'].startswith("Количество слов не может быть меньше нуля."))

    def test_204_status_code(self):
        WordsViewSet.allowed_words_languages.append('fr')
        response = self.client.get(reverse('words-list') + '?language=fr', format='json')
        self.assertEqual(response.status_code, 204)

    def test_default_language(self):
        WordsViewSet.default_language = 'eng'
        response = self.client.get(reverse('words-list'), format='json')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response['language'], 'eng')
