from src.domain.device import DeviceBase, DeviceCreate
from src.domain.protection_system import ProtectionSystemBase
from src.repository.device import DeviceRepository
from src.repository.protection_system import ProtectionSystemRepository

from tests.integration.repository.common import DBTestBase


class TestDeviceRepository(DBTestBase):
    """CRUD Tests for DeviceRepository class"""

    @staticmethod
    def _create_device_fixture(
        name="test device",
        protection_system: ProtectionSystemBase | None = None,
    ) -> DeviceBase:
        if protection_system is None:
            protection_system = TestDeviceRepository._create_protection_system_fixture()
        device_create = DeviceCreate(
            name=name, protection_system_id=protection_system.id
        )
        return DeviceRepository.create(device_create)

    @staticmethod
    def _create_protection_system_fixture(
        name="test protection system", encryption_mode="test encryption_mode"
    ) -> ProtectionSystemBase:
        new_protection_system = ProtectionSystemBase(
            name=name,
            encryption_mode=encryption_mode,
        )
        return ProtectionSystemRepository.create(new_protection_system)

    def test_create(self):
        protection_system = self._create_protection_system_fixture()
        device = self._create_device_fixture(
            name="test device", protection_system=protection_system
        )

        assert (
            device.id == 1
        )  # should be 1 because the DB is reset everytime. Otherwise remove (flakyness)
        assert device.protection_system == protection_system
        assert device.name == "test device"

    def test_get(self):
        device = self._create_device_fixture()
        read_device = DeviceRepository.get(device.id)
        assert read_device == device
