from pydantic import BaseModel

from src.domain.protection_system import ProtectionSystem


class ContentBase(BaseModel):
    encryption_key: str
    encrypted_payload: bytes
    is_encrypted: bool = False


class ContentCreate(ContentBase):
    protection_system_id: int


class Content(ContentBase):
    id: int
    protection_system: ProtectionSystem

    class Config:
        from_attributes = True
