from pydantic import BaseModel

from domain.protection_system import ProtectionSystem


class DeviceBase(BaseModel):
    name: str
    protection_system: ProtectionSystem


class Device(DeviceBase):
    id: int
