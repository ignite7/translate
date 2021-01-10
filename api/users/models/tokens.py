""" Tokens user models. """

# Django REST framework
from rest_framework import exceptions
from rest_framework.authentication import (
    TokenAuthentication,
    get_authorization_header
)

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.conf import settings

# Models
from api.utils.models import CommonModel

# Utilities
import jwt


class TokenModel(CommonModel):
    """
    This class it gonna handle to
    save the token of the user.
    """

    class Modes(models.TextChoices):
        IS_AUTHENTICATED = 'IA', _('is_authenticated')
        EMAIL_CONFIRMATION = 'EC', _('email_confirmation')
        RESET_PASSWORD = 'RP', _('reset_password')

    user = models.ForeignKey(
        'users.UserModel',
        on_delete=models.CASCADE,
        help_text='Info users.'
    )

    mode = models.CharField(
        max_length=2,
        choices=Modes.choices,
        default=Modes.IS_AUTHENTICATED
    )

    key = models.TextField(
        unique=True,
        help_text='Key token.'
    )

    class Meta:
        """
        Override the name.
        """

        verbose_name_plural = 'Tokens'

    def __str__(self) -> str:
        return 'Username: {}, Key: {}, Mode: {}'.format(
            self.user,
            self.key,
            self.mode
        )
