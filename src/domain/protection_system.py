from pydantic import BaseModel


class ProtectionSystemBase(BaseModel):
    name: str
    encryption_mode: str


class ProtectionSystem(ProtectionSystemBase):
    id: int

    class Config:
        from_attributes = True
