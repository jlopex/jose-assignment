from http import HTTPStatus

from fastapi.testclient import TestClient

from src.api import app
from src.domain.protection_system import ProtectionSystemBase
from src.repository.protection_system import ProtectionSystemRepository
from tests.integration.repository.common import DBTestBase


class TestProtectionSystemApi(DBTestBase):
    """Test Protection System API"""

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

    def test_get_protection_system(self):
        self._create_protection_system()
        response = self.client.get(
            f"/api/protection-systems/{self.protection_system.id}"
        )
        assert response.status_code == 200
        assert response.json() == self.protection_system.model_dump()

    def test_get_protection_system_not_found(self):
        response = self.client.get("/api/protection-systems/1")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_create_protection_system(self):
        response = self.client.post(
            "/api/protection-systems/",
            json={
                "name": "fake protection system",
                "encryption_mode": "fake encryption mode",
            },
        )

        assert response.status_code == HTTPStatus.CREATED

        protection_system = ProtectionSystemRepository.get(id=response.json()["id"])
        assert response.json() == protection_system.model_dump()
