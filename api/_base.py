from typing import Final

from fastapi import FastAPI

__all__ = ("app", "BASE_ROUTE")


app: Final[FastAPI] = FastAPI()
BASE_ROUTE: Final[str] = (
    "/api"  # Could have uses "/api/v1" but better do versioning in Headers
)
