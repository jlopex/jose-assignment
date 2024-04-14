from fastapi.testclient import TestClient

from src.api import app
from src.domain.protection_system import ProtectionSystemBase
from src.repository import db  # noqa
from src.repository.protection_system import ProtectionSystemRepository
from tests.integration.common import DBTestBase


class TestProtectionSystemApi(DBTestBase):
    """Test protection system API"""

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
