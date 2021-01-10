""" Models serializer auth. """

# Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


# Django
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator

# Models
from api.users.models.users import UserModel
from api.users.models.tokens import TokenModel


class UserModelSerializer(serializers.ModelSerializer):
    """ User model serializer class. """

    class Meta:
        """ override meta class. """

        model = UserModel
        fields = (
            'email',
            'username',
            'is_verified',
            'first_name',
            'last_name',
            'phone',
            'picture'
        )


class UserCredentialsModelSerializer(serializers.ModelSerializer):
    """ User credentials model serializer class. """

    email = serializers.EmailField(
        max_length=254,
        label='Email',
        help_text='Email field.'
    )

    token = serializers.CharField(
        source='key',
        label='Token',
        help_text='Token field.'
    )

    class Meta:
        """ Override meta class. """

        model = TokenModel
        fields = (
            'email',
            'token'
        )


class AccountInfoModelSerializer(serializers.Serializer):
    """ Account info model serializer. """

    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=UserModel.objects.all())],
        label='Email',
        help_text='Email field.'
    )

    username = serializers.CharField(
        min_length=4,
        max_length=25,
        validators=[
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=UserModel.objects.all())
        ],
        label='Username',
        help_text='Username field.'
    )

    first_name = serializers.CharField(
        min_length=2,
        max_length=150,
        required=False,
        label='First name',
        help_text='First name filed.'
    )

    last_name = serializers.CharField(
        min_length=2,
        max_length=150,
        required=False,
        label='Last name',
        help_text='Last name filed.'
    )

    picture = serializers.ImageField(
        required=False,
        label='Picture',
        help_text='Picture field.'
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Format: +9 99999999 Up to 15 digits allowed.')
    )

    phone = serializers.CharField(
        max_length=15,
        required=False,
        validators=[phone_regex],
        label='Phone',
        help_text='Phone field'
    )

    password = serializers.CharField(
        min_length=12,
        label='Password',
        help_text='Password field.'
    )

    password_confirmation = serializers.CharField(
        min_length=12,
        label='Password confirmation',
        help_text='Password confirmation field.'
    )
