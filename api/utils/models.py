""" Utils models. """

# Django
from django.db import models


class CommonModel(models.Model):
    """ Common class model. """

    is_used = models.BooleanField(
        default=True,
        help_text='By default everything will be active.'
    )

    created_at = models.DateTimeField(
        name='created_at',
        auto_now_add=True,
        help_text='When it has been created.'
    )

    modified_at = models.DateTimeField(
        name='modified_at',
        auto_now=True,
        help_text='When it has been modified.'
    )

    class Meta:
        """ Meta class. """

        abstract = True
        get_latest_by = 'created_at',
        ordering = [
            '-created_at',
            '-modified_at'
        ]
