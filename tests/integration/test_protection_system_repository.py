from src.domain.protection_system import ProtectionSystemBase
from tests.integration.common import DBTestBase
from src.repository.protection_system import ProtectionSystemRepository

class TestProtectionSystemRepository(DBTestBase):
    def test_create(self):
        new_protection_system = ProtectionSystemBase(
            name="test_protection_system",
            encryption_mode="test_protection_system",
        )
        protection_system = ProtectionSystemRepository.create(new_protection_system)
        assert protection_system.id == 1  # Must be always 1 since the DB is clean
        assert {
           "id": 1, **new_protection_system.model_dump()
        } == protection_system.model_dump()


