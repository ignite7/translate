""" Account serializer. """

# Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Django
from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password

# Modules
from api.utils.tokens import token_manager

# Models
from api.users.models.users import UserModel

# Serializers
from api.users.serializers.commmons import (
    UserModelSerializer,
    AccountInfoModelSerializer
)

# Tasks
from api.tasks.users.auth.tasks import send_email_confirmation
from api.tasks.users.accounts.tasks import send_reset_password


class GetAccountSerializer(serializers.Serializer):
    """ Get account serializer class. """

    def validate(self, attrs: dict) -> dict:
        """ Validate username from query params. """

        username = self.context['username']
        payload = token_manager.get_or_create_token(username)
        self.context['payload'] = payload

        return attrs

    def retrieve(self) -> dict:
        """ Returns user info. """

        return self.context['payload'][1]['user']


class UpdateAccountSerializer(AccountInfoModelSerializer):
    """ Update account serializer class. """

    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=UserModel.objects.all())],
        required=False,
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
        required=False,
        label='Username',
        help_text='Username field.'
    )

    password = serializers.CharField(
        min_length=12,
        required=False,
        label='Password',
        help_text='Password field.'
    )

    password_confirmation = serializers.CharField(
        min_length=12,
        required=False,
        label='Password confirmation',
        help_text='Password confirmation field.'
    )

    def validate(self, attrs: dict) -> dict:
        """ Validate data. """

        # Password and password confirmations are the same
        if attrs.get('password') and attrs.get('password_confirmation'):
            if attrs['password'] != attrs['password_confirmation']:
                raise serializers.ValidationError('Passwords do not match.')
            password_validation.validate_password(attrs['password'])

        if attrs.get('password') and not attrs.get('password_confirmation'):
            raise serializers.ValidationError('Needs password confirmation.')

        if attrs.get('email'):
            validate_email(attrs['email'])

        return attrs

    def update(self, validated_data: dict) -> dict:
        """ Update user. """

        attrs = validated_data
        user = self.context['request'].user

        # Update user fields.
        if attrs.get('email') and attrs.get('email') != user.email:
            user.email = attrs['email']
            user.verified_email = False

        if attrs.get('password'):
            user.password = make_password(attrs['password'])

        user.username = attrs.get('username', user.username)
        user.first_name = attrs.get('first_name', user.first_name)
        user.last_name = attrs.get('last_name', user.last_name)
        user.picture = attrs.get('picture', user.picture)
        user.phone = attrs.get('phone', user.phone)
        user.save()

        if attrs.get('email'):
            payload = token_manager.get_or_create_token(user.email, mode='EC')
            send_email_confirmation.delay(
                payload[1]['user'],
                payload[1]['authorization']['token']
            )
            token_manager.delete_token_by_modes(
                {'instance': user}, ['IA', 'RP']
            )

            return {
                'user': UserModelSerializer(user).data,
                'verification': 'Confirm your email in 24h.'
            }

        if attrs:
            return {
                'user': UserModelSerializer(user).data,
                'message': 'User updated successfully.'
            }
        else:
            return {'message': 'No changes.'}


class SendResetPasswordSerializer(serializers.Serializer):
    """ Send reset password serializer class. """

    email = serializers.EmailField(
        max_length=254,
        label='Email',
        help_text='Email field.'
    )

    def validate(self, attrs: dict) -> dict:
        """ Validate email. """

        validate_email(attrs['email'])

        return attrs

    def create(self, validated_data: dict) -> dict:
        """ Send email to reset password. """

        attrs = validated_data
        payload = token_manager.get_or_create_token(
            attrs['email'],
            mode='RP',
            view='send_reset_password'
        )
        send_reset_password.delay(
            payload[1]['user'],
            payload[1]['authorization']['token']
        )

        # Delete other token modes
        token_manager.delete_token_by_modes(payload[0]['user'], ['IA', 'EC'])

        return {
            'email': attrs['email'],
            'message': f'Reset your password in 3h'
        }


class ResetPasswordSerializer(serializers.Serializer):
    """ Reset password serializer class. """

    token = serializers.CharField(
        label='Token',
        help_text='Token field.'
    )

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

    password_confirmation = serializers.CharField(
        min_length=12,
        label='Password confirmation',
        help_text='Password confirmation field.'
    )

    def validate(self, attrs: dict) -> dict:
        """ Validate password. """

        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError('Passwords do not match')

        validate_email(attrs['email'])
        password_validation.validate_password(attrs['password'])

        return attrs

    def update(self, validated_data: dict) -> dict:
        """ Update password """

        attrs = validated_data
        payload = token_manager.get_or_create_token(
            attrs['email'],
            attrs['token'],
            'RP',
            'reset_password'
        )
        user = payload[0]['user']['instance']

        # Check password is not the old user password
        if user.check_password(attrs['password']):
            raise serializers.ValidationError('Use different password.')

        user.password = make_password(attrs['password'])
        user.save()
        token_manager.delete_token_by_modes(payload[0]['user'])

        return {
            'user': payload[0]['user']['json'],
            'message': 'Password changed successfully.'
        }
