from django.db import models


class Address(models.Model):
    region = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )

    district = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )

    city = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )

    township = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )

    zipcode = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )

    street = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )

    house = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )

    building = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )

    apartment = models.CharField(
        max_length=2047,
        blank=True,
        null=False,
        default="",
    )
