from typing import Final

from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

__all__ = ("app", "BASE_ROUTE")

from src.common.unicorn_exception import UnicornException

app: Final[FastAPI] = FastAPI()
BASE_ROUTE: Final[str] = (
    "/api"  # Could have uses "/api/v1" but better do versioning in Headers
)


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """Implements a custom exception handler as defined here:
    https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
    """
    if exc.__class__.__name__ == "RepositoryNotFoundError":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)}
        )

    if exc.__class__.__name__ == "SecurityInvalidProtection":
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(exc)}
        )

    # unhandled error
    return JSONResponse(
        status_code=500,
        content={"message": f"Error: {exc.name}"},
    )
