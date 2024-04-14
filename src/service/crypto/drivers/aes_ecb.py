import random

from src.service.crypto.drivers.base import BaseCryptoDriver


class AesEcbDriver(BaseCryptoDriver):
    @staticmethod
    def name() -> str:
        return "AES+ECB"

    @staticmethod
    def get_superkey(key: str) -> bytes:
        key_b = bytes(ord(x) % 256 for x in key)
        gkey = AesEcbDriver.global_key() + key_b
        return bytes(x for tup in zip(key_b, gkey) for x in tup)

    @staticmethod
    def encrypt(plaintext: bytes, key: str) -> bytes:
        key_b = AesEcbDriver.get_superkey(key)
        seed = AesEcbDriver.hash(key_b)
        random.seed(seed)

        return bytes(
            random.randint(0, 255) ^ x ^ key_b[i % len(key_b)]
            for i, x in enumerate(plaintext)
        )

    @staticmethod
    def decrypt(ciphertext: bytes, key: str) -> bytes:
        return AesEcbDriver.encrypt(ciphertext, key)  # It's symmetrical
