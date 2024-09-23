import os

from apps.campaigns.repositories.orm import MegaDirection as ORMMegaDirection
from apps.campaigns.repositories.university import (
    MegaDirection as UniversityMegaDirection,
)
from apps.utils.adapters.university_adapter import UniversityAdapter
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Load MegaDirections from 1C"

    def handle(self, *args, **options):
        # TODO should be constructed from configuration
        service = UniversityAdapter(
            protocol=os.getenv("ODATA_PROTOCOL"),
            host=os.getenv("ODATA_HOST"),
            port=os.getenv("ODATA_PORT"),
            infobase=os.getenv("ODATA_INFOBASE"),
            user=os.getenv("ODATA_USER"),
            password=os.getenv("ODATA_PASSWORD"),
        )
        with transaction.atomic():
            ORMMegaDirection.deactivate_all()
            for mega_direction in UniversityMegaDirection.load_entities(
                service
            ):
                ORMMegaDirection(mega_direction).persist()
