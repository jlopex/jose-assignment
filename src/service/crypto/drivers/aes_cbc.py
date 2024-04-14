import random

from src.service.crypto.drivers._base import BaseCryptoDriver


class AesCbcDriver(BaseCryptoDriver):
    @staticmethod
    def name() -> str:
        return "AES+CBC"

    @staticmethod
    def encrypt(plaintext: bytes, key: str) -> bytes:
        key_b = bytes(ord(x) % 256 for x in key)
        seed = AesCbcDriver.hash(key_b)
        random.seed(seed)

        return bytes(
            random.randint(0, 255) ^ x ^ key_b[i % len(key_b)]
            for i, x in enumerate(plaintext)
        )

    @staticmethod
    def decrypt(ciphertext: bytes, key: str) -> bytes:
        return AesCbcDriver.encrypt(ciphertext, key)  # It's symmetrical
