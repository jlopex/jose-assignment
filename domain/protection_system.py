from pydantic import BaseModel


class ProtectionSystem(BaseModel):
    id_: int
    name: str
    encryption_mode: str
