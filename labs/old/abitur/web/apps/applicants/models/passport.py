from django.db import models

from .person import Person


class Passport(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        null=False,
        primary_key=True,
    )

    series = models.CharField(
        max_length=255,
        default="",
        blank=True,
        null=False,
    )

    number = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    issuer = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        default="",
    )

    issuer_code = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        default="",
    )

    issued_date = models.DateField(
        null=False,
    )
