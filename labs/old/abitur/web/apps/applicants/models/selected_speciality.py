from django.db import models

from .applicant import Applicant
from .speciality import Speciality


class SelectedSpeciality(models.Model):

    applicant = models.ForeignKey(
        Applicant,
        db_index=True,
        default=None,
        null=False,
        on_delete=models.CASCADE,
        related_name="selected_specialities",
    )

    speciality = models.ForeignKey(
        Speciality,
        default=None,
        null=False,
        on_delete=models.CASCADE,
    )
