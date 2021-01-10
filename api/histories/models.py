""" History models. """

# Django
from django.db import models

# Models
from api.utils.models import CommonModel
from api.users.models.users import UserModel

# Languages
from cli.utils.languages import languages_tuple

# Utilities
import uuid


class HistoryBaseModel(models.Model):
    """ History base model class. """

    text = models.TextField(
        help_text='Text input.'
    )

    class Meta:
        """ Override meta class. """

        abstract = True


class HistoryTranslationsModel(HistoryBaseModel, CommonModel):
    """ History translations model. """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    history = models.ManyToManyField(
        UserModel,
        related_name='translations_users_histories'
    )

    favorite = models.ManyToManyField(
        UserModel,
        related_name='translations_users_favorites'
    )

    translation = models.TextField(
        help_text='Translated message.'
    )

    source = models.CharField(
        max_length=36,
        choices=languages_tuple,
        help_text='Source language code.'
    )

    target = models.CharField(
        max_length=36,
        choices=languages_tuple,
        help_text='Target language code.'
    )

    word_count = models.PositiveIntegerField(
        help_text='Estimate of the number of words in the input text.'
    )

    character_count = models.PositiveIntegerField(
        help_text='Number of characters in the input text.'
    )

    class Meta:
        """ Override name class. """

        verbose_name_plural = 'HistoryTranslations'

    def __str__(self) -> str:
        return 'ID: {}, Source: {}, Target: {}'.format(
            self.pk,
            self.source,
            self.target
        )


class HistoryIdentifyModel(HistoryBaseModel, CommonModel):
    """ History identify model. """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    history = models.ManyToManyField(
        UserModel,
        related_name='identify_users_histories'
    )

    favorite = models.ManyToManyField(
        UserModel,
        related_name='identify_users_favorites'
    )

    identify_languages = models.JSONField()

    class Meta:
        """ Override name class. """

        verbose_name_plural = 'HistoryIdentify'

    def __str__(self) -> str:
        return 'ID: {}, Identify languages: {}'.format(
            self.pk,
            self.identify_languages,
        )
