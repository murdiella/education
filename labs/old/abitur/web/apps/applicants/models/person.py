import re

from apps.geography.models import Address
from django.db import models

from .applicant import Applicant


class Person(models.Model):

    applicant = models.OneToOneField(
        Applicant,
        on_delete=models.CASCADE,
        primary_key=True,
        null=False,
    )

    firstname = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    lastname = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    middlename = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        default="",
    )

    UNKNOWN = "UN"
    MALE = "ML"
    FEMALE = "FM"

    GENDER_CHOICES = [
        (UNKNOWN, "UNKNOWN"),
        (MALE, "MALE"),
        (FEMALE, "FEMALE"),
    ]

    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=UNKNOWN,
    )

    date_of_birth = models.DateField(
        null=False,
    )

    place_of_birth = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )

    phone = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    no_address = models.BooleanField(
        default=False,
        null=False,
    )
