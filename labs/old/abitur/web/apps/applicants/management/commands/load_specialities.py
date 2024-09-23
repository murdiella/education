from apps.applicants.models import Speciality
from apps.geography.repositories.university.repository import (
    UniversityRepository,
)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load Specialities from 1C"

    def handle(self, *args, **options):
        specialities = []
        for speciality in UniversityRepository().load_entities(Speciality):
            self.stdout.write(str(speciality))
            specialities.append(speciality)
