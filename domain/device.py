from pydantic import BaseModel

from domain.protection_system import ProtectionSystem


class Device(BaseModel):
    id_: int
    name: str
    protection_system: ProtectionSystem

