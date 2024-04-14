from src.domain.content import Content, ContentCreate
from src.domain.protection_system import ProtectionSystemBase
from src.repository.content import ContentRepository
from src.repository.protection_system import ProtectionSystemRepository
from tests.integration.repository.common import DBTestBase


class TestContentRepository(DBTestBase):
    """CRUD Tests for ContentRepository class"""

    _BLOB_FIXTURE = bytes([x for y in range(2) for x in range(256)])
    _ENCRYPTION_KEY = "fake encryption key"

    def _create_content_fixture(
        self,
        protection_system: ProtectionSystemBase | None = None,
    ) -> Content:
        if protection_system is None:
            protection_system = self._create_protection_system_fixture()
        content_create = ContentCreate(
            encryption_key=self._ENCRYPTION_KEY,
            encrypted_payload=self._BLOB_FIXTURE,
            protection_system_id=protection_system.id,
            is_encrypted=True,
        )
        return ContentRepository.create(content_create)

    @staticmethod
    def _create_protection_system_fixture(
        name="test protection system", encryption_mode="test encryption_mode"
    ) -> ProtectionSystemBase:
        new_protection_system = ProtectionSystemBase(
            name=name,
            encryption_mode=encryption_mode,
        )
        return ProtectionSystemRepository.create(new_protection_system)

    def test_create(self):
        protection_system = self._create_protection_system_fixture()
        content = self._create_content_fixture(protection_system=protection_system)

        assert (
            content.id == 1
        )  # should be 1 because the DB is reset everytime. Otherwise, remove (flakyness)
        assert content.protection_system == protection_system
        assert content.encryption_key == self._ENCRYPTION_KEY
        assert content.encrypted_payload == self._BLOB_FIXTURE

    def test_get(self):
        content = self._create_content_fixture()
        read_content = ContentRepository.get(content.id)
        assert read_content == content
