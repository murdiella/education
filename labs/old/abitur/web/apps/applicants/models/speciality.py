from django.db import models


class Speciality(models.Model):
    ref = models.CharField(
        max_length=2047,
        default=None,
        null=False,
        db_index=True,
        unique=True,
    )

    mega_direction_number = models.CharField(
        max_length=2,
        default="1",
        null=False,
        blank=False,
    )

    mega_direction_name = models.CharField(
        max_length=255,
        default="Авиастроение",
        null=False,
        blank=False,
    )

    name = models.CharField(
        max_length=255,
        default=None,
        blank=False,
        null=False,
    )

    code = models.CharField(
        max_length=255,
        default=None,
        blank=False,
        null=False,
    )

    system_code = models.CharField(
        max_length=255,
        default="",
        blank=False,
        null=False,
    )
