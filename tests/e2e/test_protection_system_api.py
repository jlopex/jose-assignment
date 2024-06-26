from http import HTTPStatus

from fastapi.testclient import TestClient

from src.api import app
from src.repository.protection_system import ProtectionSystemRepository
from tests.factory.protection_system import ProtectionSystemFactory
from tests.integration.repository.common import DBTestBase


class TestProtectionSystemApi(DBTestBase):
    """Test Protection System API"""

    def setup_class(self):
        self.client = TestClient(app)

    def test_get_protection_system(self):
        protection_system = ProtectionSystemFactory.new()
        response = self.client.get(f"/api/protection-systems/{protection_system.id}")
        assert response.status_code == 200
        assert response.json() == protection_system.model_dump()

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

    def test_list_all_protection_systems(self):
        protection_systems = [
            ProtectionSystemFactory.new(name="PS1"),
            ProtectionSystemFactory.new(name="PS2"),
        ]

        response = self.client.get("/api/protection-systems/")
        assert response.json() == [
            ps.model_dump() for ps in protection_systems
        ]  # potential flakiness

    def test_filter_protection_systems_by_name(self):
        protection_systems = [
            ProtectionSystemFactory.new(name="PS1"),
            ProtectionSystemFactory.new(name="PS2"),
        ]

        response = self.client.get("/api/protection-systems/", params={"name": "PS1"})
        assert response.json() == [protection_systems[0].model_dump()]
