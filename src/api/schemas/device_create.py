from src.domain.device import DeviceCreate


class DeviceCreateSchema(DeviceCreate):
    name: str
    protection_system_id: int
