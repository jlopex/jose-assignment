from src.domain.device import Device, DeviceCreate
from src.repository import model
from src.repository.db import generic_create, generic_get, generic_list, generic_delete

__all__ = ("DeviceRepository",)


class DeviceRepository:
    @staticmethod
    def create(new_device: DeviceCreate) -> Device:
        db_device = model.Device(
            name=new_device.name, protection_system_id=new_device.protection_system_id
        )
        return generic_create(db_device, Device)

    @staticmethod
    def get(id: int) -> Device:
        return generic_get(id, model.Device, Device)

    @staticmethod
    def find(**kwargs) -> list[Device]:
        return generic_list(model.Device, Device, **kwargs)

    @staticmethod
    def delete(id: int):
        generic_delete(model.Device, id=id)
