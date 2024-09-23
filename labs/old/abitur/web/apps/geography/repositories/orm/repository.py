from apps.geography.domain.entites import Country
from apps.geography.models import Country as CountryORM
from apps.utils.domain import Repository


class ORMRepository(Repository):
    @staticmethod
    def load_entity(cls, **kwargs):
        if cls == Country:
            orm_object = CountryORM.objects.get(**kwargs)
            return Country(
                ref=orm_object.ref,
                name=orm_object.name,
                code=orm_object.code,
            )

    @staticmethod
    def load_entities(cls):
        result = []
        if cls == Country:
            orm_objects = CountryORM.objects.all()
            for obj in orm_objects:
                country = Country(
                    ref=obj.ref,
                    name=obj.name,
                    code=obj.code,
                )
                result.append(country)
        return result
