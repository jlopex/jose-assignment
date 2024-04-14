# Implements a dummy crypto service
from typing import TypeVar

from src import config
from src.domain.content import Content, ContentCreate
from .drivers.aes_cbc import AesCbcDriver
from .drivers.aes_ecb import AesEcbDriver
from .drivers.base import BaseCryptoDriver
from ...domain.protection_system import ProtectionSystem
from ...repository.protection_system import ProtectionSystemRepository

_T = TypeVar("_T", Content, ContentCreate)


class CryptoService:
    DRIVER = {
        AesCbcDriver.name(): AesCbcDriver,
        AesEcbDriver.name(): AesEcbDriver,
    }

    @classmethod
    def get_driver(cls, name: str) -> BaseCryptoDriver:
        if name not in cls.DRIVER:
            raise NotImplementedError(f"Crypto driver [{name}] not implemented.")

        return cls.DRIVER[name]

    @staticmethod
    def get_secret() -> bytes:
        return config.CRYPTO_KEY

    @classmethod
    def _encrypt(cls, driver: str, content: bytes, key: str) -> bytes:
        return cls.get_driver(driver).encrypt(content, key)

    @classmethod
    def _decrypt(cls, driver: str, content: bytes, key: str) -> bytes:
        return cls.get_driver(driver).decrypt(content, key)

    @classmethod
    def _get_protection_system(cls, content: _T) -> ProtectionSystem:
        if isinstance(content, Content):
            return content.protection_system

        return ProtectionSystemRepository.get(content.protection_system_id)

    @classmethod
    def _assemble_content(
        cls, content: _T, encrypted_payload: bytes, *, is_encrypted: bool
    ) -> _T:
        attrs = content.model_dump(exclude={"encrypted_payload", "is_encrypted"})

        if isinstance(content, ContentCreate):
            return ContentCreate(
                **attrs, is_encrypted=is_encrypted, encrypted_payload=encrypted_payload
            )

        return Content(
            **attrs,
            is_encrypted=is_encrypted,
            encrypted_payload=encrypted_payload,
        )

    @classmethod
    def encrypt(cls, content: _T) -> _T:
        if content.is_encrypted:
            return content

        protection_system = cls._get_protection_system(content)
        encrypted_payload = cls._encrypt(
            protection_system.encryption_mode,
            content.encrypted_payload,
            content.encryption_key,
        )

        return cls._assemble_content(
            content=content, encrypted_payload=encrypted_payload, is_encrypted=True
        )

    @classmethod
    def decrypt(cls, content: _T) -> _T:
        if not content.is_encrypted:
            return content

        protection_system = cls._get_protection_system(content)
        encrypted_payload = cls._decrypt(
            protection_system.encryption_mode,
            content.encrypted_payload,
            content.encryption_key,
        )

        return cls._assemble_content(
            content=content, encrypted_payload=encrypted_payload, is_encrypted=False
        )
