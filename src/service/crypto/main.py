# Implements a dummy crypto service
from src import config
from src.domain.content import Content
from .drivers.aes_cbc import AesCbcDriver
from .drivers.aes_ecb import AesEcbDriver
from .drivers.base import BaseCryptoDriver


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
    def encrypt(cls, content: Content) -> Content:
        if content.is_encrypted:
            return content

        return Content(
            id=content.id,
            encrypted_payload=cls._encrypt(
                content.protection_system.encryption_mode,
                content.encrypted_payload,
                content.encryption_key,
            ),
            is_encrypted=True,
            encryption_key=content.encryption_key,
            protection_system=content.protection_system,
        )

    @classmethod
    def decrypt(cls, content: Content) -> Content:
        if not content.is_encrypted:
            return content

        return Content(
            id=content.id,
            encrypted_payload=cls._decrypt(
                content.protection_system.encryption_mode,
                content.encrypted_payload,
                content.encryption_key,
            ),
            is_encrypted=False,
            encryption_key=content.encryption_key,
            protection_system=content.protection_system,
        )
