from src.domain.content import Content, ContentCreate
from src.domain.protection_system import ProtectionSystem
from src.repository.content import ContentRepository
from src.service.crypto import CryptoService
from tests.factory.protection_system import ProtectionSystemFactory


class ContentFactory:
    @staticmethod
    def new(
        encryption_key: str = "dummy key",
        encrypted_payload: bytes = b"dummy payload",
        protection_system: ProtectionSystem | None = None,
        protection_system_id: int | None = None,
    ) -> Content:
        if protection_system is None and protection_system_id is None:
            protection_system = ProtectionSystemFactory.new()

        if protection_system_id is None:
            protection_system_id = protection_system.id
        elif protection_system:
            assert (
                protection_system.id == protection_system_id
            ), "Invalid Fixture initialization"

        content_create = ContentCreate(
            encryption_key=encryption_key,
            encrypted_payload=encrypted_payload,
            protection_system_id=protection_system_id,
        )
        encrypted_content = CryptoService.encrypt(content_create)
        return ContentRepository.create(encrypted_content)
