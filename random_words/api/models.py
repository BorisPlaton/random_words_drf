from django.db import models


class WordsLanguage(models.TextChoices):
    """Available words languages."""
    ENG = 'eng'
    UA = 'ua'
    RU = 'ru'


class Word(models.Model):
    """The models for words on different languages."""

    word = models.CharField("Word", max_length=32)
    language = models.CharField(
        "Word language", choices=WordsLanguage.choices,
        max_length=8, db_index=True
    )

    class Meta:
        verbose_name = 'Word'
        verbose_name_plural = 'Words'
        constraints = [
            models.CheckConstraint(
                name='check_word_language_is_valid',
                check=models.Q(language__in=WordsLanguage.values)
            ),
            models.UniqueConstraint(
                name='word_with_its_language_is_unique',
                fields=['word', 'language']
            )
        ]

    def __str__(self):
        return self.word
