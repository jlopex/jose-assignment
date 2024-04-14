from http import HTTPStatus
from io import BytesIO

from fastapi.testclient import TestClient

from src.api import app
from tests.factory.content import ContentFactory
from tests.factory.device import DeviceFactory
from tests.factory.protection_system import ProtectionSystemFactory
from tests.integration.repository.common import DBTestBase


class TestContentApi(DBTestBase):
    """Tests Content API"""

    def setup_class(self):
        self.client = TestClient(app)

    def test_get_content(self):
        device = DeviceFactory.new()
        payload = b"fake payload"
        content = ContentFactory.new(
            encrypted_payload=payload, protection_system=device.protection_system
        )
        response = self.client.get(
            f"/api/content/{content.id}", params={"device_id": 1}
        )

        assert response.status_code == 200
        assert response.content == payload

    def test_get_content_not_found(self):
        response = self.client.get("/api/content/1", params={"device_id": 1})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_create_content(self):
        file = BytesIO(b"Hello world")
        protection_system = ProtectionSystemFactory.new()
        response = self.client.post(
            f"/api/content/{protection_system.id}/upload/FAKE_KEY",
            files={"file": ("test_image.png", file, "image/jpeg")},
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {"filename": "test_image.png", "id": 1, "size": 11}
