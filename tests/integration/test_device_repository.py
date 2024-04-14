from src.domain.device import DeviceBase
from src.domain.protection_system import ProtectionSystemBase
from src.repository.device import DeviceRepository
from src.repository.protection_system import ProtectionSystemRepository

from tests.integration.common import DBTestBase


class TestDeviceRepository(DBTestBase):
    """CRUD Tests for DeviceRepository class"""

    def test_create(self):
        new_protection_system = ProtectionSystemBase(
            name="test_protection_system",
            encryption_mode="test_protection_system",
        )
        protection_system = ProtectionSystemRepository.create(new_protection_system)
        device_create = DeviceBase(
            name="test device", protection_system=protection_system
        )
        device = DeviceRepository.create(device_create)

        assert (
            device.id == 1
        )  # should be 1 because the DB is reset everytime. Otherwise remove (flakyness)
        assert device.protection_system == protection_system
        assert device.name == "test device"
