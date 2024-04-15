from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.api import app
from src.repository.content import ContentRepository
from src.repository.exceptions import RepositoryNotFoundError
from src.service.crypto import CryptoService
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
            f"/api/contents/{content.id}", params={"device_id": 1}
        )

        assert response.status_code == 200
        assert response.json() == {
            "payload": "fake payload",
            "protectionSystem": "fake protection system",
            "symmetricKey": "dummy key",
        }

    def test_get_content_not_found(self):
        response = self.client.get("/api/contents/1", params={"device_id": 1})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_create_content(self):
        protection_system = ProtectionSystemFactory.new()
        response = self.client.post(
            f"/api/contents/",
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
        response = self.client.delete(f"/api/contents/{content.id}")

        assert response.status_code == HTTPStatus.ACCEPTED
        with pytest.raises(RepositoryNotFoundError):
            ContentRepository.get(content.id)

    def test_update_content(self):
        content = ContentFactory.new()
        response = self.client.put(
            f"/api/contents/{content.id}",
            json={
                "protectionSystem": content.protection_system.name,
                "payload": "NEW TEST PAYLOAD",
                "symmetricKey": "123",
            },
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"id": 1, "message": "encrypted", "size": 16}

        updated_content = ContentRepository.get(content.id)
        decrypted_content = CryptoService.decrypt(updated_content)

        assert decrypted_content.encrypted_payload == b"NEW TEST PAYLOAD"
