from pydantic import BaseModel

from src.domain.protection_system import ProtectionSystem


class DeviceBase(BaseModel):
    name: str


class DeviceCreate(DeviceBase):
    protection_system_id: int


class Device(DeviceBase):
    id: int
    protection_system: ProtectionSystem

    class Config:
        from_attributes = True
