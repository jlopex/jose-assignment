from src.domain.device import Device, DeviceBase
from src.repository import model
from src.repository.db import generic_create, generic_get

__all__ = ("DeviceRepository",)


class DeviceRepository:
    @staticmethod
    def create(new_device: DeviceBase) -> Device:
        db_device = model.Device(
            name=new_device.name, protection_system_id=new_device.protection_system.id
        )
        return generic_create(db_device, Device)

    @staticmethod
    def get(id: int) -> Device:
        return generic_get(id, model.Device, Device)
