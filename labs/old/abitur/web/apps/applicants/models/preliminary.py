from django.db import models

from .applicant import Applicant


class PreliminaryForm(models.Model):
    applicant = models.OneToOneField(
        Applicant,
        on_delete=models.CASCADE,
        null=False,
        primary_key=True,
        related_name="preliminary_form",
    )

    need_dormitory = models.BooleanField(
        default=False,
        null=False,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    sent = models.BooleanField(
        null=False,
        default=False,
    )
