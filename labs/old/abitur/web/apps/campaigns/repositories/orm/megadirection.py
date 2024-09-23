from apps.campaigns.domain.entites import MegaDirection as Entity
from apps.campaigns.models import MegaDirection as Model


class MegaDirection:
    def __init__(
        self,
        entity: Entity,
    ):
        self._entity = entity

    @property
    def ref(self):
        return self._entity.ref

    @property
    def name(self):
        return self._entity.name

    @property
    def number(self):
        return self._entity.number

    @property
    def contacts(self):
        return self._entity.contacts

    @property
    def active(self):
        return self._entity.active

    def persist(self):
        orm_object = Model.objects.get_or_create(ref=self.ref)
        orm_object.name = self.name
        orm_object.number = self.number
        orm_object.contacts = self.contacts
        orm_object.active = self.active
        orm_object.full_clean()
        orm_object.save()

    @staticmethod
    def deactivate_all():
        Model.objects.all().update(active=False)
