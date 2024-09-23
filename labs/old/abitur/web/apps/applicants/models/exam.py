from django.db import models

from .applicant import Applicant


class Exam(models.Model):
    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        db_index=True,
        null=False,
        related_name="exams",
    )

    EGE = "EG"
    INTERNAL_EXAM = "IN"

    EXAM_CHOICES = [
        (EGE, "ege"),
        (INTERNAL_EXAM, "internal exam"),
    ]

    type = models.CharField(
        max_length=2,
        null=False,
        choices=EXAM_CHOICES,
    )

    year = models.PositiveIntegerField(
        null=False,
    )

    mark = models.PositiveIntegerField(
        null=True,
    )

    subject = models.CharField(
        max_length=2,
        null=False,
        blank=False,
    )
