from pydantic import BaseModel

from src.domain.protection_system import ProtectionSystem


class ContentBase(BaseModel):
    protection_system: ProtectionSystem
    encryption_key: str
    encryption_payload: bytes


class Content(ContentBase):
    id: int
