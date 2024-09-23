import os
import re

from apps.applicants.models import Speciality
from apps.geography.domain.entities import Country
from apps.utils.adapters.university_adapter import UniversityAdapter
from apps.utils.domain import Repository

service = UniversityAdapter(
    protocol=os.getenv("ODATA_PROTOCOL"),
    host=os.getenv("ODATA_HOST"),
    port=os.getenv("ODATA_PORT"),
    infobase=os.getenv("ODATA_INFOBASE"),
    user=os.getenv("ODATA_USER"),
    password=os.getenv("ODATA_PASSWORD"),
)


class UniversityRepository(Repository):
    def load_entity(self, cls, ref):
        raise NotImplementedError

    def load_entities(self, cls):
        result = []
        if cls == Country:
            countries = service.pull("СтраныМира")
            for country in countries:
                name = (
                    country["НаименованиеПолное"]
                    or country["Description"].title()
                )
                if not name:
                    continue
                entity = Country(
                    ref=country["Ref_Key"],
                    code=country["Code"],
                    name=name,
                )
                result.append(entity)

        if cls == Speciality:
            megadirections = service.pull("МАИ_МегаНаправления")
            specialities = service.pull("Специальности")

            md = {}
            for megadirection in megadirections:
                md[megadirection["Ref_Key"]] = {
                    "code": megadirection["Code"],
                    "name": megadirection["Description"],
                }

            for speciality in specialities:
                ref = speciality["Ref_Key"]
                code = speciality["КодСпециальности"]
                print(speciality["Description"])
                name = speciality["Description"]
                name = re.sub('[.0-9"]', "", name).strip()
                print(name)
                megadirection_ref = speciality["МАИ_Меганаправление_Key"]
                try:
                    megadirection = md[megadirection_ref]
                except KeyError:
                    continue
                try:
                    obj = Speciality.objects.get(ref=ref)
                except Speciality.DoesNotExist:
                    obj = Speciality(ref=ref)
                obj.code = code
                obj.name = name
                obj.system_code = speciality["Code"]
                obj.mega_direction_name = megadirection["name"]
                obj.mega_direction_code = megadirection["code"]
                obj.full_clean()
                obj.save()
                result.append(obj)

            result.append(speciality)

        return result
