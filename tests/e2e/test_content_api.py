from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.api import app
from src.repository.content import ContentRepository
from src.repository.exceptions import RepositoryNotFoundError
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
        assert response.json() == {
            "payload": "fake payload",
            "protectionSystem": "fake protection system",
            "symmetricKey": "dummy key",
        }

    def test_get_content_not_found(self):
        response = self.client.get("/api/content/1", params={"device_id": 1})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_create_content(self):
        protection_system = ProtectionSystemFactory.new()
        response = self.client.post(
            f"/api/content/",
            json={
                "protectionSystem": protection_system.name,
                "payload": "test payload",
                "symmetricKey": "123",
            },
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {"message": "encrypted", "id": 1, "size": 12}

    def test_delete_content(self):
        content = ContentFactory.new()
        response = self.client.delete(f"/api/content/{content.id}")

        assert response.status_code == HTTPStatus.ACCEPTED
        with pytest.raises(RepositoryNotFoundError):
            ContentRepository.get(content.id)
