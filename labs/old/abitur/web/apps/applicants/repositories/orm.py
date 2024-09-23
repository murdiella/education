from apps.utils.domain import Repository


class ORMRepository(Repository):
    def load_entity(self, cls, ref):
        return None

    def load_entities(self, cls):
        return []
