from pydantic import BaseModel


class NewDeviceSchema(BaseModel):
    name: str
    protection_system_id: int
