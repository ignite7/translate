""" Accounts tasks. """

# Django REST framework
from rest_framework import status

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Celery
from celery import shared_task

# Models
from api.users.models.tokens import TokenModel

# Utilities
import jwt


@shared_task(name='send reset password', max_retries=3)
def send_reset_password(user: dict, token: str) -> int:
    """ Send email confirmation task. """

    subject = f'Hello @{user["email"]}, reset your password in Translate'
    from_email = f'Translate <{settings.EMAIL_HOST}>'
    content = render_to_string(
        'emails/accounts/send_reset_password.html',
        {'host': settings.ALLOWED_HOSTS[0], 'user': user, 'token': token}
    )
    msg = EmailMultiAlternatives(
        subject, content, from_email, [user['email']]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send()

    return status.HTTP_200_OK


@shared_task(name='clean ec and ia tokens')
def clean_ec_and_ia_tokens() -> int:
    """ Clean tokens `EC` and `IA` each 24h. """

    email_confirmation = TokenModel.objects.filter(mode='EC')
    is_authenticated = TokenModel.objects.filter(mode='IA')

    if not email_confirmation and not is_authenticated:
        return status.HTTP_404_NOT_FOUND

    for tokens in email_confirmation, is_authenticated:
        for token in tokens:
            try:
                jwt.decode(
                    jwt=token.key,
                    key=settings.SECRET_KEY,
                    algorithms='HS256'
                )
            except jwt.ExpiredSignatureError:
                # Delete account and token
                if token.mode == 'EC':
                    token.user.delete()
                # Delete token only
                else:
                    token.delete()
            except jwt.PyJWTError:
                token.delete()

    return status.HTTP_204_NO_CONTENT


@shared_task(name='clean rp tokens')
def clean_rp_tokens() -> int:
    """ Clean token `RP` each 3h. """

    reset_password = TokenModel.objects.filter(mode='RP')

    if not reset_password:
        return status.HTTP_404_NOT_FOUND

    for token in reset_password:
        try:
            jwt.decode(
                jwt=token.key,
                key=settings.SECRET_KEY,
                algorithms='HS256'
            )
        except jwt.ExpiredSignatureError:
            token.delete()
        except jwt.PyJWTError:
            token.delete()

    return status.HTTP_204_NO_CONTENT
