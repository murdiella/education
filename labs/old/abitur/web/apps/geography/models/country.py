from django.db import models


class Country(models.Model):
    code = models.CharField(
        null=False,
        blank=False,
        max_length=7,
        db_index=True,
    )

    name = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        default=None,
    )

    ref = models.CharField(
        null=False,
        blank=False,
        max_length=2047,
        default=None,
    )
