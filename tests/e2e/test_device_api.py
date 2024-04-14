from http import HTTPStatus

from fastapi.testclient import TestClient

from src.api import app
from src.repository.device import DeviceRepository
from tests.factory.device import DeviceFactory
from tests.factory.protection_system import ProtectionSystemFactory
from tests.integration.repository.common import DBTestBase


class TestDeviceApi(DBTestBase):
    """Test Device API"""

    def setup_class(self):
        self.client = TestClient(app)

    def test_get_device(self):
        device = DeviceFactory.new()
        response = self.client.get(f"/api/devices/{device.id}")

        assert response.status_code == 200
        assert response.json() == device.model_dump()

    def test_get_device_not_found(self):
        response = self.client.get("/api/devices/1")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_create_device(self):
        protection_system = ProtectionSystemFactory.new()
        response = self.client.post(
            "/api/devices/",
            json={
                "name": "fake device",
                "protection_system_id": protection_system.id,
            },
        )

        assert response.status_code == HTTPStatus.CREATED

        device = DeviceRepository.get(id=response.json()["id"])
        assert response.json() == device.model_dump()
