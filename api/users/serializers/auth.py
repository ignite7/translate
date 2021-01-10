""" Auth serializers. """

# Django REST framwork
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.contrib.auth import authenticate, password_validation

# Models
from api.users.models.users import UserModel

# Modules
from api.utils.tokens import token_manager

# Serializers
from api.users.serializers.commmons import (
    UserCredentialsModelSerializer,
    AccountInfoModelSerializer
)

# Tasks
from api.tasks.users.auth.tasks import send_email_confirmation


class SignupSerializer(AccountInfoModelSerializer):
    """ Sign up serializer class. """

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

    def validate(self, attrs: dict) -> dict:
        """ Validate data. """

        # Password and password confirmations are the same
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError(
                'Passwords does not macth.'
            )

        validate_email(attrs['email'])
        password_validation.validate_password(attrs['password'])

        return attrs

    def create(self, validated_data: dict) -> dict:
        """ Create user """

        attrs = validated_data

        # Create user
        user = UserModel.objects.create_user(
            email=attrs['email'],
            username=attrs['username'],
            password=attrs['password'],
            is_verified=False,
            verified_email=False,
            first_name=attrs.get('first_name', ''),
            last_name=attrs.get('last_name', ''),
            phone=attrs.get('phone', ''),
            picture=attrs.get('picture', '')
        )

        # Create token email confirmation
        payload = token_manager.get_or_create_token(user.email, mode='EC')

        # Send email confirmation
        send_email_confirmation.delay(
            payload[0]['user']['json'],
            payload[0]['token'].key
        )

        return {
            'user': payload[1]['user'],
            'verification': 'Confirm your email in 24h.'
        }


class LoginSerializer(serializers.Serializer):
    """ Login serializer class. """

    email = serializers.EmailField(
        max_length=254,
        label='Email',
        help_text='Email field.'
    )

    password = serializers.CharField(
        min_length=12,
        label='Password',
        help_text='Password field.'
    )

    def validate(self, attrs: dict) -> dict:
        """ Validate data. """

        user = authenticate(
            username=attrs['email'],
            password=attrs['password']
        )

        # Check credentials
        if not user:
            raise serializers.ValidationError('Invalied credentials.')

        if not user.verified_email:
            raise serializers.ValidationError('Email is not verified yet.')

        self.context['user'] = user

        return attrs

    def create(self) -> dict:
        """ Create login token. """

        user = self.context['user']
        payload = token_manager.get_or_create_token(user.email)

        return payload[1]


class EmailConfirmationSerializer(UserCredentialsModelSerializer):
    """ Email confirmation serializer class. """

    def validate(self, attrs: dict) -> dict:
        """ Validate token. """

        validate_email(attrs['email'])

        return attrs

    def update(self, validated_data: dict) -> dict:
        """ Update verified email account. """

        attrs = validated_data
        payload = token_manager.get_or_create_token(
            attrs['email'], attrs['key'], 'EC'
        )
        user = payload[0]['user']['instance']
        user.verified_email = True
        user.save()
        token_manager.delete_token(
            payload[0]['user'], payload[0]['token'].key, 'EC'
        )

        return {
            'user': payload[1]['user'],
            'message': 'Email verified successfully.'
        }
