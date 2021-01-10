""" Auth tasks. """

# Django REST framework
from rest_framework import status

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Celery
from celery import shared_task


@shared_task(name='send email confirmation', max_retries=3)
def send_email_confirmation(user: dict, token: str) -> int:
    """ Send email confirmation task. """

    subject = (
        'Welcome @{}! Verify your account to start using Translate'
    ).format(user['email'])
    from_email = f'Translate <{settings.EMAIL_HOST}>'
    content = render_to_string(
        'emails/auth/send_email_confirmation.html',
        {'host': settings.ALLOWED_HOSTS[0], 'user': user, 'token': token}
    )
    msg = EmailMultiAlternatives(
        subject, content, from_email, [user['email']]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send()

    return status.HTTP_200_OK
