""" Commons user models. """

# Django REST framework
from rest_framework import exceptions
from rest_framework.authentication import (
    TokenAuthentication,
    get_authorization_header
)

# Django
from django.utils.translation import gettext_lazy as _

# Modules
from api.utils.tokens import token_manager

# Models
from api.users.models.tokens import TokenModel


class TokenBaseModel(TokenAuthentication):
    """
    This class is the token model
    of `TokenModel`.
    """

    model = TokenModel

    def authenticate(self, request):
        auth = get_authorization_header(request)

        if not auth:
            return None

        try:
            token = token_manager.authenticate(
                token_manager.split_token(auth.decode())
            )
        except UnicodeError:
            msg = _('Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
