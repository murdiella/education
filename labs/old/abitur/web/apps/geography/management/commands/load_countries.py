from apps.geography.domain.entities import Country
from apps.geography.models import Country as CountryORM
from apps.geography.repositories.university.repository import (
    UniversityRepository,
)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load Countries from 1C"

    def handle(self, *args, **options):
        countries = []
        for country in UniversityRepository().load_entities(Country):
            self.stdout.write(str(country))
            countries.append(country)
        for country in countries:
            try:
                obj = CountryORM.objects.get(ref=country.ref)
            except CountryORM.DoesNotExist:
                obj = CountryORM(ref=country.ref)
            obj.name = country.name
            obj.code = country.code
            obj.save()
