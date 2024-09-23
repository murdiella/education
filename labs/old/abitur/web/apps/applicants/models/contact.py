from django.db import models

from .person import Person


class Phone(models.Model):

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=False,
        related_name="additional_phones",
    )

    number = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
    )


class Social(models.Model):

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=False,
        related_name="social_links",
        db_index=True,
    )

    link = models.CharField(
        max_length=2047,
        null=False,
        blank=False,
    )
