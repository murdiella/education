from apps.utils.domain import Entity


class MegaDirection(Entity):
    name: str
    code: str

    def __init__(
        self,
        ref=None,
        name=None,
        repository=None,
    ):
        super().__init__(ref, repository)
