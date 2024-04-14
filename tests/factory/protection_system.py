from src.domain.protection_system import ProtectionSystemBase, ProtectionSystem
from src.repository.protection_system import ProtectionSystemRepository

__all__ = ("ProtectionSystemFactory",)


class ProtectionSystemFactory:
    @staticmethod
    def new(
        name: str = "fake protection system",
        encryption_mode: str = "AES+ECB",
    ) -> ProtectionSystem:
        new_protection_system = ProtectionSystemBase(
            name=name,
            encryption_mode=encryption_mode,
        )
        return ProtectionSystemRepository.create(new_protection_system)
