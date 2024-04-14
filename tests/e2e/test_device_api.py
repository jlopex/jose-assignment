from http import HTTPStatus

from fastapi.testclient import TestClient

from src.api import app
from src.domain.device import DeviceCreate
from src.domain.protection_system import ProtectionSystemBase
from src.repository.device import DeviceRepository
from src.repository.protection_system import ProtectionSystemRepository
from tests.integration.common import DBTestBase


class TestDeviceApi(DBTestBase):
    """Test Device API"""

    def setup_class(self):
        self.client = TestClient(app)

    def _create_protection_system(self):
        new_protection_system = ProtectionSystemBase(
            name="test_protection_system",
            encryption_mode="test_protection_system",
        )
        self.protection_system = ProtectionSystemRepository.create(
            new_protection_system
        )

    def _create_device(self):
        self._create_protection_system()
        new_device = DeviceCreate(
            name="test_device",
            protection_system_id=self.protection_system.id,
        )
        self.device = DeviceRepository.create(new_device)

    def test_get_device(self):
        self._create_device()
        response = self.client.get(f"/api/devices/{self.device.id}")
        assert response.status_code == 200
        assert response.json() == self.device.model_dump()

    def test_get_device_not_found(self):
        response = self.client.get("/api/devices/1")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_create_device(self):
        self._create_protection_system()
        response = self.client.post(
            "/api/devices/",
            json={
                "name": "fake device",
                "protection_system_id": self.protection_system.id,
            },
        )

        assert response.status_code == HTTPStatus.CREATED

        device = DeviceRepository.get(id=response.json()["id"])
        assert response.json() == device.model_dump()
