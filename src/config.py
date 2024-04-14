# Simple generic config container
from typing import Final


DB_NAME: Final[str] = "sqlite:///database.db"
DB_ECHO: Final[bool] = True

CRYPTO_KEY: Final[bytes] = b"dummy-secret-key-used-as-salt"
