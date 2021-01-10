""" User models. """

# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

# Models
from api.utils.models import CommonModel


class UserModel(CommonModel, AbstractUser):
    """
    This class it will be handle to
    implement the auth to the user.
    """

    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True,
        help_text='Email is unique.'
    )

    username = models.CharField(
        'username',
        max_length=25,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        help_text='Username field.'
    )

    password = models.TextField(
        name='password',
        help_text='Password field.'
    )

    picture = models.ImageField(
        upload_to='api/data/media/users/',
        blank=True,
        null=True,
        help_text='Picture of the user.'
    )

    verified_email = models.BooleanField(
        default=False,
        help_text='Email confirmation.'
    )

    is_verified = models.BooleanField(
        default=False,
        help_text='Verified user field.'
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Format: +9 99999999 Up to 15 digits allowed.')
    )

    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        help_text='Phone of the user.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        """ Override the name. """

        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        """ Returns username string. """

        return self.username

    def get_short_name(self) -> str:
        """ Returns short name string. """

        return self.username

    def get_full_name(self) -> str:
        """ Returns full name string. """

        return 'Username: {}, First Name: {}, Last Name: {}'.format(
            self.username,
            self.first_name,
            self.last_name
        )
