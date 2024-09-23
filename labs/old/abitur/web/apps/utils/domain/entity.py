import uuid
from typing import Optional


class Entity:
    """Models a Domain Entity.

    Domain entity is mutable; equality is defined by
    special identifier called **ref**.

    If ref is not passed during instantiation of Entity
    it will be initialized with uuid4.

    If ref and repository are passed during instantiation,
    the Entity will be loaded from the repository.
    """

    ref: str

    def __init__(
        self,
        ref: Optional[str] = None,
        repository=None,
    ):
        """Initialize Entity."""

        self.ref = ref or uuid.uuid4().hex
        if ref is not None and repository is not None:
            self.load(repository)

    def load(self, repository):
        """Load entity from the repository and update the state.

        Note: this operation will force state on the entity from
        the repository.
        """
        loaded = repository.load_entity(self.__class__, self.ref)
        for item, value in vars(loaded).items():
            self.__setattr__(item, value)

    def __eq__(self, other: object) -> bool:
        """Define Entities equality.

        Entities are considered equal if they have
        same identifier.
        """
        if not isinstance(other, self.__class__):
            raise NotImplemented
        return self.ref == other.ref

    def __str__(self):
        format_var = lambda x: f"{x[0]}={x[1]}"
        return f"{self.__class__.__name__}({', '.join(format_var(var) for var in vars(self).items())})"
