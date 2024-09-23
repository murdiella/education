from apps.utils.domain import Entity


class Country(Entity):

    name: str
    code: str

    def __init__(
        self,
        ref=None,
        name=None,
        code=None,
        repository=None,
    ):
        self.name = name
        self.code = code
        super().__init__(ref, repository)
        if name is not None:
            self.name = name
        if code is not None:
            self.code = code
