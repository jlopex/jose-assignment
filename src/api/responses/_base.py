from abc import ABC, abstractmethod
from typing import Self

from pydantic import BaseModel


class ResponseBaseMixin(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def from_entity(cls, entity: BaseModel) -> Self:
        pass
