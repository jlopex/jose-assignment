from src.domain.protection_system import ProtectionSystemBase, ProtectionSystem
from src.repository import model
from src.repository.db import generic_create, generic_get, generic_list

__all__ = ("ProtectionSystemRepository",)


class ProtectionSystemRepository:
    @staticmethod
    def create(new_protection_system: ProtectionSystemBase) -> ProtectionSystem:
        protection_system = model.ProtectionSystem(**new_protection_system.model_dump())

        return generic_create(protection_system, ProtectionSystem)

    @staticmethod
    def get(id: int) -> ProtectionSystem:
        return generic_get(id, model.ProtectionSystem, ProtectionSystem)

    @staticmethod
    def find(**kwargs) -> list[ProtectionSystem]:
        return generic_list(model.ProtectionSystem, ProtectionSystem, **kwargs)
