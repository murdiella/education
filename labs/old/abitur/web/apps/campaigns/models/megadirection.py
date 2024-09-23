from django.db import models


class MegaDirection(models.Model):

    ref = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        primary_key=True,
    )

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    number = models.CharField(
        max_length=15,
        blank=False,
        null=False,
    )

    contact_information = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )

    active = models.BooleanField(
        default=False,
        null=False,
    )
