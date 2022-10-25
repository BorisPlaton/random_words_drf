from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.services import load_new_words


class Command(BaseCommand):
    help = 'Loads words from the file to the `Word` model.'

    def add_arguments(self, parser):
        parser.add_argument('words_file', type=str, help="File with words")
        parser.add_argument('words_language', type=str, help="Words' language")

    def handle(self, *args, **options):
        try:
            with open(settings.BASE_DIR / options['words_file']) as f:
                all_words = [word.strip().lower() for word in f.readlines()]
            load_new_words(all_words, options['words_language'])
        except Exception as e:
            raise CommandError(e)
