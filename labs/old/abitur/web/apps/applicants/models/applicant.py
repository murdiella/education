from apps.geography.models import Country
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Applicant(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        null=False,
    )

    citizenship = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        default=None,
    )

    ENGLISH = "EN"
    FRENCH = "FR"
    GERMAN = "GE"

    LANGUAGE_CHOICES = [
        (ENGLISH, "english"),
        (FRENCH, "french"),
        (GERMAN, "german"),
    ]

    language = models.CharField(
        null=True,
        max_length=2,
        choices=LANGUAGE_CHOICES,
    )

    ref = models.CharField(
        null=True,
        blank=True,
        default=None,
        max_length=255,
    )
