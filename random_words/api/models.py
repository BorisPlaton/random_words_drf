from django.db import models


class Word(models.Model):
    """Модель слов на разных языках."""

    word = models.CharField("Word", max_length=15, unique=True)
    language = models.CharField("Word language", max_length=3, db_index=True)

    class Meta:
        verbose_name = 'Word'
        verbose_name_plural = 'Words'

    def __str__(self):
        return self.word
