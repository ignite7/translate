""" Restricts user models. """

# Django
from django.db import models

# Models
from api.utils.models import CommonModel


class RestrictIPModel(CommonModel):
    """
    Restrict the ip of the
    anonymous user.
    """

    ip_remote_addr = models.GenericIPAddressField(
        unique=True,
        help_text='Ip address.'
    )

    requests = models.PositiveIntegerField(
        help_text='Count the requests per hour by ip.'
    )

    class Meta:
        """
        Override the name.
        """

        verbose_name_plural = 'RetrictIP'

    def __str__(self) -> str:
        return 'IP remote address: {}, Request per day: {}'.format(
            self.ip_remote_addr,
            self.requests
        )
