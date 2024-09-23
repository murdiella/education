from django.db import models

from .person import Person


class PersonalDataProcessingAgreement(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        null=False,
        primary_key=True,
        related_name="pd_agreement",
    )

    ip = models.GenericIPAddressField(
        null=False,
    )

    timestamp = models.DateTimeField(
        null=False,
        auto_now_add=True,
    )
