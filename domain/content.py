from pydantic import BaseModel

from domain.protection_system import ProtectionSystem


class Content(BaseModel):
    id_: int
    protection_system: ProtectionSystem
    encryption_key: str
    encryption_payload: bytes
