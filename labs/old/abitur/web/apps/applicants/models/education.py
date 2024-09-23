from django.db import models

from .applicant import Applicant


class Education(models.Model):
    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        db_index=True,
        null=False,
        related_name="educations",
    )

    SCHOOL = "SC"
    COLLEGE = "CL"
    BACHELOR = "BA"
    SPECIALIST = "SP"
    MASTER = "MA"

    LEVEL_CHOICES = [
        (SCHOOL, "school"),
        (COLLEGE, "college"),
        (BACHELOR, "bachelor"),
        (SPECIALIST, "specialist"),
        (MASTER, "master"),
    ]

    level = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        choices=LEVEL_CHOICES,
    )

    CERTIFICATE = "CT"
    DIPLOMA = "DP"

    DOCUMENT_TYPE_CHOICES = [
        (CERTIFICATE, "certificate"),
        (DIPLOMA, "diploma"),
    ]

    document_type = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        choices=DOCUMENT_TYPE_CHOICES,
    )

    series = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        default="",
    )

    number = models.CharField(
        max_length=255,
        blank=True,
        null=False,
    )

    issued_date = models.DateField(
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=2047,
        null=False,
        blank=False,
    )

    year = models.PositiveIntegerField(
        blank=False,
        null=False,
    )

    original = models.BooleanField(
        default=False,
    )
