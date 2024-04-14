from src.domain.protection_system import ProtectionSystemBase, ProtectionSystem
from src.repository.db import generic_create
from src.repository import model

__all__ = ('ProtectionSystemRepository', )


class ProtectionSystemRepository:
    @staticmethod
    def create(new_protection_system: ProtectionSystemBase) -> ProtectionSystem:
        protection_system = model.ProtectionSystem(**new_protection_system.model_dump())

        return generic_create(
            protection_system,
            ProtectionSystem
        )
