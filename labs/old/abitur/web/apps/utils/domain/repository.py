from abc import ABC, abstractmethod
from typing import List, Type, TypeVar

T = TypeVar("T")


class Repository(ABC):
    @abstractmethod
    def load_entity(self, cls: Type[T], ref: str) -> T:
        pass

    @abstractmethod
    def load_entities(self, cls: Type[T]) -> List[T]:
        return []
