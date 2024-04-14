from typing import Self

from src.api.responses._base import ResponseBaseMixin
from src.domain.device import Device


class DeviceResponse(ResponseBaseMixin, Device):
    @classmethod
    def from_entity(cls, entity: Device) -> Self:
        return cls(**entity.model_dump())
