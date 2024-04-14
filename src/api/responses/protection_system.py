from typing import Self

from src.api.responses._base import ResponseBaseMixin
from src.domain.protection_system import ProtectionSystem


class ProtectionSystemResponse(ResponseBaseMixin, ProtectionSystem):
    @classmethod
    def from_entity(cls, entity: ProtectionSystem) -> Self:
        return cls(**entity.model_dump())
