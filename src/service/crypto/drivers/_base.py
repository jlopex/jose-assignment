from abc import ABC, abstractmethod


class BaseCryptoDriver(ABC):
    """Implements the Crypto Driver interface.
    NOTE: Crypto Drivers implemented here are for illustrative purposes. DO NOT USE in real projects!
    """

    @staticmethod
    def hash(item: bytes) -> int:
        """Dummy (unsecure) repeatable hash function"""
        length = 8
        h = [0] * length
        for i, x in enumerate(item):
            h[i % length] ^= x

        return int("".join("%02X" % i for i in h), 16)

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def encrypt(data: bytes, key: str) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def decrypt(data: bytes, key: str) -> bytes:
        pass
