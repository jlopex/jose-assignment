import pytest

from src.domain.content import Content
from src.domain.protection_system import ProtectionSystem
from src.service import crypto


class TestCryptoService:
    def _new_protection_system(
        self, name: str = "AES 1", encryption_mode: str = "AES+ECB"
    ) -> ProtectionSystem:
        return ProtectionSystem(id=1, name=name, encryption_mode=encryption_mode)

    def _new_content(
        self,
        encryption_key: str = "fake key",
        encrypted_payload: bytes = b"fake payload",
        protection_system: ProtectionSystem | None = None,
        is_encrypted: bool = False,
    ):
        if protection_system is None:
            protection_system = self._new_protection_system()

        return Content(
            id=1,
            encryption_key=encryption_key,
            encrypted_payload=encrypted_payload,
            protection_system=protection_system,
            is_encrypted=is_encrypted,
        )

    def test_raises_error_for_non_existing_crypto_driver(self):
        with pytest.raises(NotImplementedError):
            crypto.CryptoService.get_driver("dummy-non-existing-driver")

    def test_call_driver_to_encrypt_content_if_not_encrypted(self):
        result = crypto.CryptoService.encrypt(self._new_content(is_encrypted=False))
        assert result.is_encrypted
        assert result.encrypted_payload == b"\x1fl\xffZ~8\x1e\xc2\x12,\xbc\xfd"

    def test_do_not_call_driver_to_encrypt_content_if_encrypted(self):
        result = crypto.CryptoService.encrypt(self._new_content(is_encrypted=True))
        assert result.is_encrypted
        assert result.encrypted_payload == b"fake payload"  # should remain unchanged

    def test_call_driver_to_decrypt_content_if_encrypted(self):
        result = crypto.CryptoService.decrypt(
            self._new_content(
                is_encrypted=True,
                encrypted_payload=b"\x1fl\xffZ~8\x1e\xc2\x12,\xbc\xfd",
            )
        )
        assert not result.is_encrypted
        assert result.encrypted_payload == b"fake payload"

    def test_do_not_call_driver_to_decrypt_content_if_decrypted(self):
        result = crypto.CryptoService.decrypt(
            self._new_content(
                is_encrypted=False,
                encrypted_payload=b"\x1fl\xffZ~8\x1e\xc2\x12,\xbc\xfd",
            )
        )
        assert not result.is_encrypted
        assert (
            result.encrypted_payload == b"\x1fl\xffZ~8\x1e\xc2\x12,\xbc\xfd"
        )  # should remain unchanged
