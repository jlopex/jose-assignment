from src.domain.device import DeviceCreate, Device
from src.domain.protection_system import ProtectionSystem
from src.repository.device import DeviceRepository
from tests.factory.protection_system import ProtectionSystemFactory

__all__ = ("DeviceFactory",)


class DeviceFactory:
    @staticmethod
    def new(
        name: str = "test device",
        protection_system_id: int | None = None,
        protection_system: ProtectionSystem | None = None,
    ) -> Device:
        if protection_system is None and protection_system_id is None:
            protection_system = ProtectionSystemFactory.new()

        if protection_system_id is None:
            protection_system_id = protection_system.id

        if protection_system_id is not None and protection_system is not None:
            assert (
                protection_system_id == protection_system.id
            ), "Invalid Fixture initialization"

        new_device = DeviceCreate(
            name=name,
            protection_system_id=protection_system_id,
        )

        return DeviceRepository.create(new_device)
