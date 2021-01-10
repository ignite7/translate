""" Tokens utils. """

# Django REST framework
from rest_framework import exceptions

# Django
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Models
from api.users.models.users import UserModel
from api.users.models.tokens import TokenModel

# Serializers
from api.users.serializers.commmons import UserModelSerializer

# Utilities
from typing import NoReturn, Union
import datetime
import jwt


class TokenManager:
    """ Token manager class. """

    secret_key = settings.SECRET_KEY
    algorithm = 'HS256'

    @staticmethod
    def split_token(token: str) -> str:
        """ Resturns the token separated. """

        key = token.split()

        if len(key) == 1:
            return key[0]

        else:
            if len(key) > 2:
                raise exceptions.AuthenticationFailed(
                    'Token string should not contain spaces.'
                )

            if key[0].lower() != 'token':
                raise exceptions.AuthenticationFailed(
                    'Invalid keyword token.'
                )

            return key[1]

    @staticmethod
    def token_exists(user: dict, token: str,
                     mode: str = 'IA') -> TokenModel:
        """
        Returns a instance of `TokenModel`
        otherwise raise error `NotFound`.
        """

        get_token = get_object_or_404(
            TokenModel,
            user=user['instance'],
            mode=mode,
            key=TokenManager.split_token(token)
        )

        return get_token

    def formatted_msg(self, payload: dict, mode: str = 'IA') -> dict:
        """ Format payload to readeable JSON. """

        return {
            'authorization': {
                'token': f'Token {payload["token"].key}',
                'mode': payload['mode'][mode],
                'expiration_date': payload['mode']['exp_date']
            },
            'user': payload['user']['json']
        }

    def get_user(self, auth: str) -> dict:
        """
        Get a user depending of the
        `email` or `username` and
        returns an instance of
        `UserModel`.
        """

        user = get_object_or_404(
            UserModel,
            Q(email=auth) | Q(username=auth)
        )

        return {'instance': user, 'json': UserModelSerializer(user).data}

    def get_mode(self, mode: str = 'IA') -> dict:
        """
        Get the mode authentification
        that are: [`IA`, `EC`, `RP`],
        and returns the details of the
        mode.
        """

        if mode == 'IA':
            time = datetime.datetime.now() + datetime.timedelta(hours=1)
            name = {mode: 'is_authenticated'}
            unix_time = {'timestamp': time}
            exp_date = {
                'exp_date': unix_time['timestamp'].strftime(
                    '%m-%d-%Y, %H:%M:%S UTC'
                )
            }
        elif mode == 'EC':
            time = datetime.datetime.now() + datetime.timedelta(hours=24)
            name = {mode: 'email_confirmation'}
            unix_time = {'timestamp': time}
            exp_date = {
                'exp_date': unix_time['timestamp'].strftime(
                    '%m-%d-%Y, %H:%M:%S UTC'
                )
            }
        else:
            time = datetime.datetime.now() + datetime.timedelta(hours=3)
            name = {mode: 'reset_password'}
            unix_time = {'timestamp': time}
            exp_date = {
                'exp_date': unix_time['timestamp'].strftime(
                    '%m-%d-%Y, %H:%M:%S UTC'
                )
            }

        return name | unix_time | exp_date

    def expiration_date_handler(self, user: dict,
                                token: TokenModel,
                                mode: str = 'IA',
                                view: str = '') -> Union[dict, NoReturn]:
        """
        Check the expidation date of the token
        depending of the mode will be generated
        a new token or not.
        """

        # Generate new token.
        if mode == 'IA' or (mode == 'RP' and view == 'send_reset_password'):
            self.delete_token(user, token.key, mode)
            return self.create_payload(user, mode)

        # Only raise exception.
        elif mode == 'RP' and view == 'reset_password':
            raise exceptions.PermissionDenied('Token expired.')

        # Delete account.
        else:
            get_object_or_404(UserModel, user=user['instance']).delete()
            raise exceptions.PermissionDenied(
                'Your account and token has been deleted '
                'due to never was confirmed email.'
            )

    def get_payload(self, user: dict, token: TokenModel,
                    mode: str = 'IA', view: str = '') -> Union[dict, NoReturn]:
        """
        Get the info of the encoded token
        and returns its information.
        """

        kind = self.get_mode(mode)

        try:
            token_info = jwt.decode(
                jwt=token.key,
                key=self.secret_key,
                algorithms=self.algorithm
            )

            if token_info['user']['email'] != user['instance'].email:
                raise exceptions.PermissionDenied()

            if token_info['mode'] != kind[mode]:
                raise exceptions.AuthenticationFailed('Invalid token.')

            return {'user': user, 'mode': kind, 'token': token}

        except jwt.ExpiredSignatureError:
            return self.expiration_date_handler(user, token, mode, view)

        except jwt.PyJWTError:
            raise exceptions.NotFound('Token not found.')

    def create_payload(self, user: dict, mode: str = 'IA') -> dict:
        """ Create a new payload. """

        kind = self.get_mode(mode)
        payload = {
            'user': user['json'],
            'mode': kind[mode],
            'exp': kind['timestamp']
        }
        new_token = jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm=self.algorithm
        )
        token = TokenModel.objects.create(
            user=user['instance'],
            mode=mode,
            key=new_token
        )

        return {'user': user, 'mode': kind, 'token': token}

    def get_or_create_token(self, auth: str,
                            token: str = '',
                            mode: str = 'IA',
                            view: str = '') -> tuple[dict, dict]:
        """ Get or create token. """

        user = self.get_user(auth)

        # Verify the token belongs to the user.
        if token:
            TokenManager.token_exists(user, token, mode)

        get_token = TokenModel.objects.filter(
            user=user['instance'],
            mode=mode
        )

        # Get the current token.
        if get_token:
            payload = self.get_payload(
                user, get_token[0], get_token[0].mode, view
            )

        # Create new token.
        else:
            payload = self.create_payload(user, mode)

        return (payload, self.formatted_msg(payload, mode))

    def delete_token(self, user: dict, token: str,
                     mode: str = 'IA') -> None:
        """ Delete token. """

        get_object_or_404(
            TokenModel,
            user=user['instance'],
            mode=mode,
            key=TokenManager.split_token(token)
        ).delete()

    def delete_token_by_modes(self, user: dict,
                              modes: list = ['IA', 'EC', 'RP']) -> None:
        """ Delete token by modes. """

        for mode in modes:
            token = TokenModel.objects.filter(
                user=user['instance'],
                mode=mode
            )

            if token:
                token.delete()

    def authenticate(self, token: str) -> str:
        """
        Handle the authentication from
        the model `TokenBaseModel`.
        """

        get_token = get_object_or_404(
            TokenModel, key=token, mode='IA'
        )
        user = self.get_user(get_token.user.email)
        payload = self.get_payload(
            user, get_token, 'IA'
        )

        return payload['token'].key


token_manager = TokenManager()
